from __future__ import annotations

import json
import os
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import PipelineModel, UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/reports/upload", tags=["reports"])


async def _parse_summary(report_type: str, content: bytes) -> dict:
    report_type = report_type.lower()
    if report_type == "junit":
        root = ET.fromstring(content.decode("utf-8", errors="ignore"))
        failures = 0
        tests = 0
        for suite in root.iter("testsuite"):
            tests += int(suite.attrib.get("tests", 0))
            failures += int(suite.attrib.get("failures", 0))
        return {
            "tests_total": tests,
            "tests_failed": failures,
            "build_artifact_present": True,
        }

    if report_type == "sarif":
        payload = json.loads(content.decode("utf-8", errors="ignore"))
        critical = 0
        for run in payload.get("runs", []):
            for result in run.get("results", []):
                level = (result.get("level") or "").lower()
                if level in {"error", "critical"}:
                    critical += 1
        return {
            "critical_findings": critical,
            "build_artifact_present": True,
        }

    return {
        "bytes": len(content),
        "build_artifact_present": True,
    }


@router.post("")
async def upload_report(
    pipeline_id: int = Form(...),
    type: str = Form(...),
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)

    pipeline = await session.get(PipelineModel, pipeline_id)
    if pipeline is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found")

    content = await file.read()
    summary = await _parse_summary(type, content)

    settings = get_settings()
    storage_dir = Path(settings.REPORT_STORAGE_DIR)
    storage_dir.mkdir(parents=True, exist_ok=True)
    extension = Path(file.filename or "report.bin").suffix or ".bin"
    artifact_name = f"{uuid.uuid4().hex}{extension}"
    artifact_path = storage_dir / artifact_name
    artifact_path.write_bytes(content)

    report = await repository.create_report(
        pipeline_id=pipeline_id,
        report_type=type,
        summary_json=summary,
        artifact_ref=str(artifact_path),
    )

    return {
        "id": report.id,
        "pipeline_id": report.pipeline_id,
        "type": report.type,
        "summary_json": report.summary_json,
        "artifact_ref": report.artifact_ref,
        "uploaded_by": current_user.id,
    }

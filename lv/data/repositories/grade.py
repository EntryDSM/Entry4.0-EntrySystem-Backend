from typing import Any, Dict, Type

from pypika import Parameter, Query

from lv.data.db.mysql import MySQLClient
from lv.data.db.tables import applicant_score_tbl
from lv.services.repository_interfaces.grade import (
    DiligenceGradeRepositoryInterface,
    GradeRepositoryInterface,
)


class DiligenceGradeRepository(DiligenceGradeRepositoryInterface):
    def __init__(self, db: Type[MySQLClient] = MySQLClient):
        self.db = db

    async def get_one(self, email: str) -> Dict[str, Any]:
        query: str = Query.from_(applicant_score_tbl).select(
            applicant_score_tbl.volunteer_time,
            applicant_score_tbl.full_cut_count,
            applicant_score_tbl.period_cut_count,
            applicant_score_tbl.late_count,
            applicant_score_tbl.early_leave_count
        ).where(
            applicant_score_tbl.applicant_email == Parameter("%s")
        ).get_sql(quote_char=None)

        return await self.db.fetchone(query, email)

    async def patch(self, email: str, target: Dict[str, Any]):
        query = Query.update(applicant_score_tbl).where(
            applicant_score_tbl.applicant_email == Parameter("%s")
        )

        for col in target:
            query = query.set(col, target[col])

        await self.db.execute(query.get_sql(quote_char=None), email)


class GradeRepository(GradeRepositoryInterface):
    def __init__(self, db: Type[MySQLClient] = MySQLClient):
        self.db = db

    async def patch(self, email: str, target: Dict[str, Any]):
        query = Query.update(applicant_score_tbl).where(
            applicant_score_tbl.applicant_email == Parameter("%s")
        )

        for col in target:
            query = query.set(col, target[col])

        await self.db.execute(query.get_sql(quote_char=None), email)
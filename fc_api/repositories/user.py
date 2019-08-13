# from datetime import date
# from typing import List
# from uuid import UUID
#
# from sqlalchemy import func

from fc_api.models.user import User
from fc_api.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session=session, model=User)

#     def get_monthly_expenses(
#             self, receiver_id: UUID, start: date, end: date
#     ) -> List[dict]:
#         query = self.session.query(
#             func.sum(ExternalPurchase.price).label('cost'),
#             func.date_part('month', ExternalPurchase.purchase_date)
#                 .label('month'),
#             func.date_part('year', ExternalPurchase.purchase_date)
#                 .label('year'),
#             ExternalPurchase.receiver_id
#         ).filter(
#             ExternalPurchase.purchase_date >= start,
#             ExternalPurchase.purchase_date <= end,
#             ExternalPurchase.receiver_id == receiver_id
#         ).order_by(
#             'year', 'month'
#         ).group_by(
#             'year', 'month'
#         )
#
#         months = query.all()
#         return [{
#             "expenses": result[0],
#             "month": int(result[1]),
#             "year": int(result[2]),
#             "receiver_id": result[3]
#         } for result in months]

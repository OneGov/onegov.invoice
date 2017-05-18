from onegov.core.orm import Base
from onegov.core.orm.mixins import TimestampMixin
from onegov.core.orm.types import UUID
from onegov.core.utils import normalize_for_url
from onegov.invoice import utils
from sqlalchemy import Column, Text
from sqlalchemy_utils import observes
from uuid import uuid4


class Invoice(Base, TimestampMixin):
    """ An invoice containing at least one item to be paid. """

    __tablename__ = 'invoices'

    #: the public id of the invoice
    id = Column(UUID, primary_key=True, default=uuid4)

    #: the polymorphic type of the invoice
    type = Column(Text, nullable=False, index=True)

    #: the title of the invoice
    title = Column(Text, nullable=False)

    #: the unique invoice code to identify the invoice through e-banking
    code = Column(Text, nullable=False, unique=True)

    #: the normalized title of the invoice for sorting
    order = Column(Text, nullable=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'order_by': order
    }

    @observes('title')
    def title_observer(self, title):
        self.order = normalize_for_url(title)

    @observes('code')
    def code_observer(self, code):
        self.esr_reference = utils.encode_invoice_code(self.code)

    @property
    def formatted_code(self):
        return utils.format_invoice_code(self.code)

    @property
    def formatted_esr_reference(self):
        return utils.format_esr_reference(self.esr_reference)

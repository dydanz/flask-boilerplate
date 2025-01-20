from marketplace import ma
from marketplace.persistence.model import Merchant


class MerchantSchema(ma.Schema):
    class Meta:
        model = Merchant
        fields = ('id', 'name', 'description', 'city', 'owner_id', 'created_at', 'updated_at')


merchant_schema = MerchantSchema()
merchants_schema = MerchantSchema(many=True)

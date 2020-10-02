from fx.models import WalletModel
from .views import get_user_preference
from .tables import SearchMember


def search_settings(request):
   print("..........search_settings.......")
   table_search =SearchMember(filter_field="",filter_field_value="")
   table_search.user_preference= get_user_preference(request.user.id)
   table_search.code_name="search-member"

   return  {'table_search_context':table_search}

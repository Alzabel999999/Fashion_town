from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet
from ..models import Withdrawal
from ..serializers import WithdrawalSerializer


class WithdrawalViewSet(GenericViewSet, ViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer

    @action(detail=False, methods=['post'])
    def create_app(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        if user.profile.role == 0:
            return Response({'error': 'wrong user role'}, status=403)
        if user.profile.balance < request.GET.get('summary', 0):
            return Response({'error': 'you have not enough money, pal'}, status=403)
        serializer = WithdrawalSerializer(queryset, many=False)
        return Response(serializer.data)

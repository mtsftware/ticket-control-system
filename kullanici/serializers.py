from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *
class KullaniciSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kullanici
        fields = ['id', 'identity_no', 'email', 'first_name', 'last_name', 'birth_date', 'phone_number', 'address', 'password', 'date_joined', 'last_login', 'is_staff', 'is_superuser']
        read_only_fields = ('id', 'date_joined', 'last_login', 'is_staff', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'min_length': 6, 'max_length': 6}}
    def validate_identity_no(self, value):
        if len(value) != 11 or not value.isdigit() or str(value)[0] == '0':
            raise serializers.ValidationError('Invalid identity number')

        digits = list(map(int, value))

        total1 = sum(digits[0:10:2])
        total2 = sum(digits[1:9:2])
        check1 = (total1 * 7 - total2) % 10
        check2 = (total1 + total2 + check1) % 10
        if check1 == digits[9] and check2 == digits[10]:
            return value
        else:
            raise serializers.ValidationError('Invalid identity number')
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(KullaniciSerializer, self).create(validated_data)
    def update(self, instance, validated_data):
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.address = validated_data.get('address', instance.address)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
class KullaniciLoginSerializer(serializers.Serializer):
    class Meta:
        model = Kullanici
        fields = ['identity_no', 'password']
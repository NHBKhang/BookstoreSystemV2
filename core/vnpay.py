import hashlib
import hmac
import urllib.parse


class VNPAY:
    request_data = {}
    response_data = {}

    def get_payment_url(self, vnpay_payment_url, secret_key):
        input_data = sorted(self.request_data.items())

        # Duyệt qua danh sách đã sắp xếp và tạo chuỗi query sử dụng urllib.parse.quote_plus để mã hóa giá trị
        query_string = ''
        seq = 0
        for key, val in input_data:
            if seq == 1:
                query_string = query_string + "&" + key + '=' + urllib.parse.quote_plus(str(val))
            else:
                seq = 1
                query_string = key + '=' + urllib.parse.quote_plus(str(val))

        # Sử dụng phương thức __hmac_sha512 để tạo mã hash từ chuỗi query và khóa bí mật
        hash_value = self.__hmac_sha512(secret_key, query_string)

        return vnpay_payment_url + "?" + query_string + '&vnp_SecureHash=' + hash_value

    def validate_response(self, secret_key):
        vnp_SecureHash = self.response_data['vnp_SecureHash']

        # Loại bỏ các tham số liên quan đến mã hash
        if 'vnp_SecureHash' in self.response_data.keys():
            self.response_data.pop('vnp_SecureHash')

        if 'vnp_SecureHashType' in self.response_data.keys():
            self.responseData.pop('vnp_SecureHashType')
        # Sắp xếp dữ liệu (inputData)
        input_data = sorted(self.response_data.items())

        has_data = ''
        seq = 0
        for key, val in input_data:
            if str(key).startswith('vnp_'):
                if seq == 1:
                    has_data = has_data + "&" + str(key) + '=' + urllib.parse.quote_plus(str(val))
                else:
                    seq = 1
                    has_data = str(key) + '=' + urllib.parse.quote_plus(str(val))
        # Tạo mã hash
        hash_value = self.__hmac_sha512(secret_key, has_data)

        print('Validate debug, HashData:' + has_data + "\n HashValue:" + hash_value + "\nInputHash:" + vnp_SecureHash)

        return vnp_SecureHash == hash_value

    @staticmethod
    def __hmac_sha512(key, data):
        byte_key = key.encode('utf-8')
        byte_data = data.encode('utf-8')

        return hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()
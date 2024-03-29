from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest


# 沙箱环境应用ID
# app_id = "2021000122677078"

# 沙箱环境密钥
# private_key = """MIIEowIBAAKCAQEAsV6mws9BoGxVyKKGeIAFOo4lqdAqG1ji/lhjSZwsM6BAf+t7w0m9ceNqwFdjOyTD6N2fYIYC+0Skwm1UAzlC8XkBnLjQKf6llhe/p6a3pctfXqzIS29hCnbHSILFPc9L1f3QBja54QlVlm853MXZRobKf36cWJGArRu1rlxj+0sfpHyNyOKDwkKYkI4SuDfvqCdLhZXd3r9EYsFo1dU5oYzXpuSLkAniuCf4KNAtbEBYkF9sRSmonAiqfZUUa3L7Dz8NGvsnN+51A2mbwaoKmHMQyke9y6yaVDAdUVonk6R4uUi6IJQ5A9tMIGwWmQw7/BjP6+6weuD8+1xjL1pQewIDAQABAoIBAFjr8v7HmUcsCPXFRVU0GWr5yLgRvIppTaPl/CDzQtW/CZcYH7wQRAHM2cAED6OfEviz4yspBGWkTFWNKglTs9QLrls77GChYbKVxWfvlTJxeyajyObIuAXe9pnLtcb/Hi3ySVBUL2w6mcYJjSC5r+xDt1Gj0A43JCOlOLhpaVaZxVjP5gCg77HpGzjITgJHXJltoetCfQ1scWFW77d27tkIoLBZA2rPLZdEzvmUOonCNghcV7DPMJ2ckFTCTpuDNWjvtLWWLGWD2vcUg09xtG0ark7AEuKD1riGXK/ZWjXpHSEb0by8uPOc9ibufi5vbFzKx8k+GNEpjQTqXnT+pYECgYEA2RRYGL3PsmkTPI5HW/SPgAK4fz9w7xxxoz8EqK2cyPZodXg0lLGxhEgiGnYBMhwGybE7J46dD7fZ2QvEIiu1y7R1b5+Zm+skMqs5kdLyPs0qqRurCAMuh5UNMrlZSE9uUJclTI9HhKMhtgGsqrSYiqCwhwof/fIuHlVxY9JGteMCgYEA0SuvCCTjMXFtF027yLIpuQFrGCA2MkQRbOwSYytY/apGB5sCFuCxkFDWgcU76DFlQT9dXVtNkV+/ghW6+p5YgrkufNc8oLaw8skDg8MLyk6v2b1V0z8PHI+pY7hOlbg/u3hmOfOsJ2D9k9iGaNyt08tNEm8xulTRzQUax8SSPokCgYAqmK9gy35CCBRaQaEHDkpKWD5T2eMTSIWT/v2vC8JEPPXqdxf6RZQL3Qu0HYvGhXFfioONE5MGTpFU4dYuzlzyCAszSCIgUlfcCXVWhAo9AI1qeZ9qBxXOTRU16uD2K3/+GGqdR1BFWq12xYVYSe/U5As/tGDqt+cM1L9XUx/E+QKBgHAG0WuvNe8ZLLA6dcR7h1UKqWz2c5BgXGTV2tM6OCNDutX/8xKFrRP596jxFbC6I9zaLwr9B4JAobTuJoJrpEP/IiLCtDnvHr4pYrSDFiF4Gz6m5PyK3XESkEpUP+J4F8o0JawMEbvVenpgkTxAVOkGDXU+EIgXPXZssXcklJ7hAoGBANjbld9gbs7iUWaw1bkmYA5A1Jc3iDoWx4BTa5I62VXXaz+D6T7njxnTZ3uuCyHbgzect9hZMPHdlo2o4egGQSBhhRJLKgF2rV/kQ2npFTdBj7ZoCdh20bOZJJbJ0jlIBEiwuRj5huLVRf2FzD/lYIUpTLwX/iVtyMW6TiXGn4tx"""
# public_key = """MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsV6mws9BoGxVyKKGeIAFOo4lqdAqG1ji/lhjSZwsM6BAf+t7w0m9ceNqwFdjOyTD6N2fYIYC+0Skwm1UAzlC8XkBnLjQKf6llhe/p6a3pctfXqzIS29hCnbHSILFPc9L1f3QBja54QlVlm853MXZRobKf36cWJGArRu1rlxj+0sfpHyNyOKDwkKYkI4SuDfvqCdLhZXd3r9EYsFo1dU5oYzXpuSLkAniuCf4KNAtbEBYkF9sRSmonAiqfZUUa3L7Dz8NGvsnN+51A2mbwaoKmHMQyke9y6yaVDAdUVonk6R4uUi6IJQ5A9tMIGwWmQw7/BjP6+6weuD8+1xjL1pQewIDAQAB"""

# 正式环境应用ID
app_id = "2021003188675037"

# 正式环境密钥
private_key = """MIIEowIBAAKCAQEAhONU7n56hkOp4jR0fVTlUs0UrL+TUZzNLkrF9ztDeRIl3bXNhEb9XbcPfPvNImvXrum25GOFGQ+1wGwsOZ19bFGuIEKTesJCMewtaVab3yaCKtqoc4h1J2Mhkoyvrvb6JMqAJKTKPOG6TCUiUdHTbwT3PDEUVCrroS3FyQMIYeaXTGL53BL/Nq6cbuH8ZmI7gud95oC9fb92mFd3IIljZaTntpYgjwNnP+xD2MhalVT3rkK2Vsk6RzOQp9wvFBcvbs64N93N84F38jmlYq0qmoGV10Gw3LVnqpmvkWR9DOd+yQhnS+7DpT2tJ01Gb5NGTzCs7mH4dZPSPYzJl2FuJQIDAQABAoIBACdSofJE6PrMEPxH62Se95Et8H1B31UaIjkdlUEYf1nXPe9CegM3gof1wJaKaGRUJymyLRWeQWduF6lOGTQfX1rrPKx9Juj/jNj6+2EdaNh6q7AEri4p5gj2s5uLF/2dRd4XMh4lyVaEsT0RC/vMLFXA0Ww1Vb+mR72VLt7Rj+xwAA3GtfjLk6jvk8ZqriHXVaW3xn7B08E2Gtw9MKCqYp1tFVf9IohEdBXyhNANGCXdWN+005+d7NjmpUGhPm0GfsmKp+ToAxmU6jHDvVkpybsnrkgd6j0xCvIdLy+6d4CZDOwxnpkokBviKfZiEf72GgpLkC6ScoB95vs3FJwkQAECgYEA7ZsMB/bItuFw8sHnUPNmgB/19uAdBu0c9UlnhuO0FlV8WzYRgWoD1JrBGTXhImCVrO+e6j4k6ks5Tw4xIcREDlSz9QAa694fVGliwMJBHYdszdoEg4rTpKbN77unLA2KRZpDGf7/ZP3zHCvP1nV1cR5y9mi8JDFaf32VwlLdXiUCgYEAjyz0GhJc9Jg0X5ShlaXkXEMSUKT9rbu119WBAIQTrvzqdMDMgWXutgEhJoKdnDOQ2wbncjhvWGiZX+siy1Ta7vBl2vH1H+uyDvV+qJQGXjF2r0D+yT6QzOnJ9psDsvwpjJgk7h0YAs+MtB2B8nBCzshokAOWNjqwDocEPpoO0AECgYAa0lPLWlpR+qTrYmQgSTma4QC8+5OLQpzwO3cKTQ35L3E4QqQ7PaJtD4MYu3JMlSaQPQRtYNJ9+Dvh5rI5I5SjIYCm+XoQgiR7POI+7C65jJ4FpsS3rKYzgfjhRQeb+3NOZBmLB7QAzIHy/icaCGxXdp53nl8OntueZKjRJNWEWQKBgEx/cE0d0py9Vf5bo5oZcNH65CZCgWf6C0auxKZJ61prt7l56cqZc9m68MNqtltnEdZ08eSNUrCh8pDVSVnqlK9lsoYxEQ9lF1X2xR29OUnKk+c/iuJrk2Jo54fjey5+nJSKFfFDiji2PC9gNLYcVRW27mdEA1YmNTsN2K66EYABAoGBAJPGcCocSwlmb6/Kn5IL/F+uMGG6cZPpxTkD4SOXV4WnmYMnIpurlWC3bMOYpfu2ZZx1lUyWm1OnI6qmtu2GZkAVoyTayvyvcAYJRZVqERtPZwwCyrSEDvKc17tp+ItfBM4bx/LqcyRSf+ew+End01vURH9JWgCBCjEm6CIwoVok"""
public_key = """MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhONU7n56hkOp4jR0fVTlUs0UrL+TUZzNLkrF9ztDeRIl3bXNhEb9XbcPfPvNImvXrum25GOFGQ+1wGwsOZ19bFGuIEKTesJCMewtaVab3yaCKtqoc4h1J2Mhkoyvrvb6JMqAJKTKPOG6TCUiUdHTbwT3PDEUVCrroS3FyQMIYeaXTGL53BL/Nq6cbuH8ZmI7gud95oC9fb92mFd3IIljZaTntpYgjwNnP+xD2MhalVT3rkK2Vsk6RzOQp9wvFBcvbs64N93N84F38jmlYq0qmoGV10Gw3LVnqpmvkWR9DOd+yQhnS+7DpT2tJ01Gb5NGTzCs7mH4dZPSPYzJl2FuJQIDAQAB"""


# 配置支付宝客户端
client_config = AlipayClientConfig()
client_config.app_id = app_id
client_config.app_private_key = private_key
client_config.alipay_public_key = public_key

# 初始化AlipayClient对象
alipay_client = DefaultAlipayClient(client_config)

# 设置订单参数
out_trade_no = "20150320010101002"
total_amount = "0.01"
subject = "AI创想师"

# 创建支付请求对象
pay_request = AlipayTradePagePayRequest()
pay_request.return_url="http://chat.menganhealth.cn/"  # 支付完成后，支付宝会将用户重定向到这个URL
pay_request.notify_url="www.baidu.com"  # 支付完成后，支付宝会向这个URL发送异步通知

# 设置支付请求参数
pay_request.biz_content={"out_trade_no": out_trade_no,
                           "product_code": "FAST_INSTANT_TRADE_PAY",
                           "total_amount": total_amount,
                           "subject": subject}

# 发送支付请求
pay_response = alipay_client.page_execute(pay_request, http_method="GET")

# 获取支付宝支付页面URL
pay_url = pay_response

print("支付宝支付页面URL:", pay_url)


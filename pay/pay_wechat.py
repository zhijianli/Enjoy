from wechatpy import WeChatPay
# from wechatpy.pay import WeChatH5Order
from wechatpy.pay import WeChatH5Pay

# 这些值应该来自你的微信支付账号
APP_ID = 'wx0ebaccb7463eb86b'
MCH_ID = '1551670731'
API_KEY = '55f30118fee8403c8e706c7755ae94a5'

wechat_pay = WeChatPay(
    appid='APP_ID',
    api_key=API_KEY,
    mch_id=MCH_ID
)

H5_PAY_RETURN_URL = "https://yourdomain.com/return_url"  # 支付完成后跳转的URL

def create_h5_order(total_fee, body, out_trade_no):
    # 创建微信H5支付订单
    h5_pay = WeChatH5Pay(wechat_pay)
    response_data = h5_pay.create_order(
        total_fee=total_fee,                 # 支付金额（单位：分）
        body=body,                           # 商品描述
        out_trade_no=out_trade_no,           # 商户订单号，确保唯一性
        notify_url="https://yourdomain.com/notify_url",  # 异步接收微信支付结果通知的回调地址
        scene_info={
            "h5_info": {
                "type": "Wap",
                "wap_url": "https://yourdomain.com",
                "wap_name": "Test Wap Name",
            }
        }
    )

    # 生成H5支付跳转链接
    mweb_url = response_data["mweb_url"]
    return mweb_url


# # 创建一个订单
# order = WeChatH5Order(
#     out_trade_no='111',   # 订单编号，应该是唯一的
#     total_fee=100,   # 订单总金额，单位是分
#     body='订单描述',   # 订单描述
#     spbill_create_ip='用户IP地址',   # 用户IP地址
#     scene_info={
#         "h5_info": {
#             "type": "Wap",
#             "wap_url": "https://www.baidu.com",
#             "wap_name": "微信支付",
#         }
#     }
# )
#
# # 调用 create_h5 得到预支付链接
# prepay_url = wechat_pay.order.create_h5(order)
#
# print(f"微信H5支付链接: {prepay_url}")

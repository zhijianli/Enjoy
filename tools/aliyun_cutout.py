# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List
from viapi.fileutils import FileUtils
from alibabacloud_imageseg20191230.client import Client as imageseg20191230Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_imageseg20191230 import models as imageseg_20191230_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> imageseg20191230Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的 AccessKey ID,
            access_key_id=access_key_id,
            # 您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        # config.endpoint = f'oss-cn-hangzhou.aliyuncs.com'
        config.endpoint = f'imageseg.cn-shanghai.aliyuncs.com'
        return imageseg20191230Client(config)

    @staticmethod
    def main(
        args: List[str],image_url
    ) -> None:
        print("image_url",image_url)
        file_utils = FileUtils("LTAI5tSb4MDsMSxgQSzAYEDt", "LegWcAIgnqSIndlJUlYDnbhm9xKiVM")
        image_url = file_utils.get_oss_url(image_url, "jpg", False)
        print(image_url)
        client = Sample.create_client("LTAI5tSb4MDsMSxgQSzAYEDt", "LegWcAIgnqSIndlJUlYDnbhm9xKiVM")
        segment_hdbody_request = imageseg_20191230_models.SegmentHDBodyRequest(
            image_url=image_url
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            result = client.segment_hdbody_with_options(segment_hdbody_request, runtime)
            return result.body.data.image_url
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    # @staticmethod
    # async def main_async(
    #     args: List[str],
    # ) -> None:
    #     client = Sample.create_client("LTAI5tSb4MDsMSxgQSzAYEDt", "LegWcAIgnqSIndlJUlYDnbhm9xKiVM")
    #     segment_hdbody_request = imageseg_20191230_models.SegmentHDBodyRequest(
    #         image_url='http://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/imageseg/SegmentHDBody/SegmentHDBody1.jpg'
    #     )
    #     runtime = util_models.RuntimeOptions()
    #     try:
    #         # 复制代码运行请自行打印 API 的返回值
    #         await client.segment_hdbody_with_options_async(segment_hdbody_request, runtime)
    #     except Exception as error:
    #         # 如有需要，请打印 error
    #         UtilClient.assert_as_string(error.message)


def cutout(image_url):
    result_url = Sample.main(sys.argv[1:], image_url)
    return result_url

if __name__ == '__main__':
    result_url = Sample.main(sys.argv[1:],"http://upload.lifeweek.com.cn/2014/0211/1392085433154.jpg")
    print("result_url",result_url)




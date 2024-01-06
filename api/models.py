from django.db import models

# Create your models here.


class BidInfo(models.Model):
    id = models.AutoField(primary_key=True)
    post_time = models.CharField("发布时间", max_length=255)
    project_name = models.TextField("项目名称")
    project_detail = models.TextField("项目概况")
    budget = models.CharField("预算金额", max_length=255)
    start_time = models.CharField("开标时间", max_length=255)
    buyer_info = models.CharField("采购人信息", max_length=255)
    project_link = models.TextField("项目链接")
    create_date = models.DateTimeField("日期", auto_now=True)

    def __str__(self):
        return "{}-{}-{}".format(self.id, self.post_time, self.project_name)

    class Meta:
        ordering = ["-id"]
        db_table = 'bid_info'
        verbose_name = "bid_info"
        verbose_name_plural = verbose_name


class ProjectList(models.Model):
    id = models.AutoField(primary_key=True)
    project_number = models.CharField("项目编号", max_length=255, unique=True)
    project_link = models.TextField("项目链接")
    create_date = models.DateTimeField("日期", auto_now=True)

    def __str__(self):
        return "{}-{}".format(self.id, self.project_number)

    class Meta:
        ordering = ["-id"]
        db_table = 'project_list'
        verbose_name = "project_list"
        verbose_name_plural = verbose_name
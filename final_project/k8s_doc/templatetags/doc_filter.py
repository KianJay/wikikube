from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

register = template.Library()


"""
mark 함수는 markdown 모듈과 mark_safe 함수를 이용하여 문자열을 HTML 코드로 변환하여 반환
이 과정을 거치면 마크다운 문법에 맞도록 HTML이 생성됨.
"""
@register.filter
# def mark(value):
#     # nl2br: 줄바꿈 문자를 <br> 태그로 변환. <Enter>를 한 번만 눌러도 줄바꿈으로 인식
#     # fenced_code: 마크다운의 소스 코드 표현을 위해 적용
#     extensions = ["nl2br", "fenced_code"]
#     return mark_safe(markdown.markdown(value, extensions=extensions))
def formatted_markdown(text):
    return mark_safe(markdownify(text))
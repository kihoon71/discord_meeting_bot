import pytest
import pytest_asyncio
import sys
import os

# 현재 스크립트 파일 기준으로 src 경로 추가
sys.path.append(os.path.abspath("../src/UTIL"))


# 이제 Text를 import 가능
from Text import Text # Text.py 파일이 존재한다고 가정

# Text 클래스의 테스트
def test_import():
    text_instance = Text()
    print(text_instance)
    assert text_instance is not None

@pytest.mark.asyncio
async def test_set_text():
    # 싱글턴 인스턴스 가져오기
    text_instance = Text()
    
    # 텍스트 추가
    await text_instance.set_text("id 1","Hello, World!")
    
    # 추가된 텍스트가 리스트에 있는지 확인
    assert text_instance.get_text('id 1') == ["Hello, World!"]

@pytest.mark.asyncio
async def test_multiple_set_text():
    text_instance = Text()
    
    # 여러 개의 텍스트를 추가
    await text_instance.set_text('id 1', "First")
    await text_instance.set_text('id 2', "Second")
    
    # 추가된 텍스트가 리스트에 올바르게 저장되었는지 확인
    text_instance.get_text('id 1') == ["Hello, World!", "First"]
    text_instance.get_text('id 2') == ["Second"]

def test_clear_text():
    text_instance = Text()
    
    # 텍스트 리스트 초기화
    text_instance.clear_text('id 1')
    
    # 리스트가 비었는지 확인
    assert 'id 1' not in text_instance.data

    text_instance.clear_text('id 2')

    assert 'id 2' not in text_instance.data


def test_is_same_instance():
    text_instance1 = Text()
    text_instance2 = Text()
    
    # 두 인스턴스가 같은지 확인
    assert text_instance1 is text_instance2
    assert text_instance1 == text_instance2
    assert id(text_instance1) == id(text_instance2)




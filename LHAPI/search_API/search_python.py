import os
import csv
import json
from datetime import datetime, timedelta

'''
확실히 사용할 수 있는 유형
통합공공임대
통합공공임대(신혼희망)
국민임대
공공임대
행복주택
행복주택(신혼희망)
장기전세
'''

# 통합공공임대 유형 판별 함수 (Python 버전)
def is_eligible_for_total_public_rental(customer_info):
    # 고객 정보
    birth_date = customer_info.get('birthDate')
    enrolled_university = customer_info.get('enrolledUniversity')
    job_seeking = customer_info.get('jobSeeking')
    family_members_count = customer_info.get('familyMembersCount')
    married = customer_info.get('married')
    marriage_date = customer_info.get('marriageDate')
    dual_income = customer_info.get('dualIncome')
    has_children = customer_info.get('hasChildren')
    children_count = customer_info.get('childrenCount')
    youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
    single_parent = customer_info.get('singleParent')
    monthly_income = customer_info.get('monthlyIncome')
    household_monthly_income = customer_info.get('householdMonthlyIncome')
    own_house = customer_info.get('ownHouse')
    assets = customer_info.get('assets')
    own_car = customer_info.get('ownCar')
    car_price = customer_info.get('carPrice')
    has_subscription_account = customer_info.get('hasSubscriptionAccount')
    subscription_start_date = customer_info.get('subscriptionStartDate')
    subscription_payment_count = customer_info.get('subscriptionPaymentCount')
    subscription_payment_amount = customer_info.get('subscriptionPaymentAmount')

    # 무주택 여부 확인
    if own_house:
        return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

    # 가구 월 평균 소득 기준 확인
    median_income_thresholds = {
        1: 2228445,
        2: 3682609,
        3: 4714657,
        4: 5729913,
        5: 6695735,
        6: 7618369,
        7: 8514994,
        8: 9411619,
    }

    if family_members_count in median_income_thresholds:
        median_income_threshold = median_income_thresholds[family_members_count]
    else:
        median_income_threshold = median_income_thresholds[8] + (family_members_count - 8) * 879534

    if household_monthly_income > median_income_threshold * 1.5:
        return False, "가구 월 평균 소득이 기준 중위소득의 150%를 초과합니다."

    # 총자산 보유 기준 확인 (34,500만원 이하)
    if assets > 345000000:
        return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

    # 자동차 가액 기준 확인 (3,708만원 이하)
    if own_car and car_price > 37080000:
        return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

    return True, "통합공공임대 자격 요건을 충족합니다."

# 통합공공임대(신혼희망) 유형 판별 함수 (Python 버전)
def is_eligible_for_total_public_rental_newlywed(customer_info):
    # 고객 정보
    birth_date = customer_info.get('birthDate')
    enrolled_university = customer_info.get('enrolledUniversity')
    job_seeking = customer_info.get('jobSeeking')
    family_members_count = customer_info.get('familyMembersCount')
    married = customer_info.get('married')
    marriage_date = customer_info.get('marriageDate')
    dual_income = customer_info.get('dualIncome')
    has_children = customer_info.get('hasChildren')
    children_count = customer_info.get('childrenCount')
    youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
    single_parent = customer_info.get('singleParent')
    monthly_income = customer_info.get('monthlyIncome')
    household_monthly_income = customer_info.get('householdMonthlyIncome')
    own_house = customer_info.get('ownHouse')
    assets = customer_info.get('assets')
    own_car = customer_info.get('ownCar')
    car_price = customer_info.get('carPrice')
    has_subscription_account = customer_info.get('hasSubscriptionAccount')
    subscription_start_date = customer_info.get('subscriptionStartDate')
    subscription_payment_count = customer_info.get('subscriptionPaymentCount')
    subscription_payment_amount = customer_info.get('subscriptionPaymentAmount')

    # 무주택 여부 확인
    if own_house:
        return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

    current_date = datetime.now()
    marriage_date_obj = datetime.strptime(marriage_date, '%Y-%m-%d')

    # 혼인 상태 및 기간 조건 확인 (혼인 중이며, 혼인 기간 7년 이내 또는 예비 신혼부부)
    current_year = current_date.year
    marriage_year = marriage_date_obj.year
    marriage_duration = current_year - marriage_year

    # 혼인 상태 확인
    if not (married and marriage_duration <= 7) and not (not married and marriage_date_obj > current_date):
        return False, "혼인 상태가 아니거나 혼인 기간이 7년을 초과하여 신혼부부 자격이 없습니다."

    # 만 6세 이하 자녀 여부 확인
    if has_children:
        youngest_child_year = datetime.strptime(youngest_child_birth_date, '%Y-%m-%d').year
        youngest_child_age = current_year - youngest_child_year
        if youngest_child_age > 6:
            return False, "만 6세 이하 자녀가 없으므로 신혼부부 자격이 없습니다."

    # 가구 월 평균 소득 기준 확인 (기준 중위소득의 100% 이하, 2인 가구는 110%)
    median_income_thresholds = {
        1: 2228445,
        2: 3682609 * 1.1,  # 2인 가구는 110%
        3: 4714657,
        4: 5729913,
        5: 6695735,
        6: 7618369,
        7: 8514994,
        8: 9411619,
    }

    if family_members_count in median_income_thresholds:
        median_income_threshold = median_income_thresholds[family_members_count]
    else:
        median_income_threshold = median_income_thresholds[8] + (family_members_count - 8) * 879534

    if household_monthly_income > median_income_threshold:
        return False, "가구 월 평균 소득이 기준 중위소득을 초과합니다."

    # 총자산 보유 기준 확인 (34,500만원 이하)
    if assets > 345000000:
        return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

    # 자동차 가액 기준 확인 (3,708만원 이하)
    if own_car and car_price > 37080000:
        return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

    return True, "통합공공임대(신혼희망) 자격 요건을 충족합니다."

# 국민임대 유형 판별 함수 (Python 버전)
def is_eligible_for_national_rental(customer_info):
    # 고객 정보
    birth_date = customer_info.get('birthDate')
    enrolled_university = customer_info.get('enrolledUniversity')
    job_seeking = customer_info.get('jobSeeking')
    family_members_count = customer_info.get('familyMembersCount')
    married = customer_info.get('married')
    marriage_date = customer_info.get('marriageDate')
    dual_income = customer_info.get('dualIncome')
    has_children = customer_info.get('hasChildren')
    children_count = customer_info.get('childrenCount')
    youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
    single_parent = customer_info.get('singleParent')
    monthly_income = customer_info.get('monthlyIncome')
    household_monthly_income = customer_info.get('householdMonthlyIncome')
    own_house = customer_info.get('ownHouse')
    assets = customer_info.get('assets')
    own_car = customer_info.get('ownCar')
    car_price = customer_info.get('carPrice')
    has_subscription_account = customer_info.get('hasSubscriptionAccount')
    subscription_start_date = customer_info.get('subscriptionStartDate')
    subscription_payment_count = customer_info.get('subscriptionPaymentCount')
    subscription_payment_amount = customer_info.get('subscriptionPaymentAmount')

    # 무주택 여부 확인
    if own_house:
        return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

    # 가구 월 평균 소득 기준 확인 (전년도 도시 근로자 가구원수별 월평균 소득의 70% 이하)
    income_thresholds = {
        1: 3134668,  # 1인가구
        2: 4332570,  # 2인가구
        3: 5039054,  # 3인가구
        4: 5773927,  # 4인가구
        5: 6142550,  # 5인가구
        6: 6694297,  # 6인가구
        7: 7246045,  # 7인가구
        8: 7797793,  # 8인가구
    }

    if family_members_count in income_thresholds:
        income_threshold = income_thresholds[family_members_count]
    else:
        income_threshold = income_thresholds[8] + (family_members_count - 8) * 879534

    if household_monthly_income > income_threshold:
        return False, "가구 월 평균 소득이 국민임대 기준 소득을 초과합니다."

    # 총자산 보유 기준 확인 (34,500만원 이하)
    if assets > 345000000:
        return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

    # 자동차 가액 기준 확인 (3,708만원 이하)
    if own_car and car_price > 37080000:
        return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

    return True, "국민임대 자격 요건을 충족합니다."

# 공공임대 유형 판별 함수 (Python 버전)
def is_eligible_for_public_rental(customer_info):
    # 고객 정보
    birth_date = customer_info.get('birthDate')
    enrolled_university = customer_info.get('enrolledUniversity')
    job_seeking = customer_info.get('jobSeeking')
    family_members_count = customer_info.get('familyMembersCount')
    married = customer_info.get('married')
    marriage_date = customer_info.get('marriageDate')
    dual_income = customer_info.get('dualIncome')
    has_children = customer_info.get('hasChildren')
    children_count = customer_info.get('childrenCount')
    youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
    single_parent = customer_info.get('singleParent')
    monthly_income = customer_info.get('monthlyIncome')
    household_monthly_income = customer_info.get('householdMonthlyIncome')
    own_house = customer_info.get('ownHouse')
    assets = customer_info.get('assets')
    own_car = customer_info.get('ownCar')
    car_price = customer_info.get('carPrice')
    has_subscription_account = customer_info.get('hasSubscriptionAccount')
    subscription_start_date = customer_info.get('subscriptionStartDate')
    subscription_payment_count = customer_info.get('subscriptionPaymentCount')
    subscription_payment_amount = customer_info.get('subscriptionPaymentAmount')

    is_eligible = False
    eligibility_reason = ""

    # 1. 공통 조건: 무주택 여부 확인
    if own_house:
        return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

    # 2. 공통 자격 조건 확인 (소득, 자산, 자동차 기준)
    # 소득 기준 확인 (전년도 도시근로자 가구원수별 월평균 소득 100% 이하)
    income_thresholds = {
        1: 3482964,  # 1인가구 기준
        2: 5415712,  # 2인가구 기준
        3: 7198649,  # 3인가구 기준
        4: 8248467,  # 4인가구 기준
        5: 8775071,  # 5인가구 기준
        6: 9563282,  # 6인가구 기준
        7: 10351493, # 7인가구 기준
        8: 11139704, # 8인가구 기준
    }

    income_threshold = income_thresholds.get(family_members_count, income_thresholds[8])

    # 맞벌이 가구의 경우 소득 기준 120%까지 허용
    if dual_income:
        income_threshold *= 1.2

    if household_monthly_income > income_threshold:
        return False, "가구 월 평균 소득이 기준을 초과합니다."

    # 자산 보유 기준 확인 (부동산 2억 1,550만 원 이하)
    if assets > 215500000:
        return False, "총 자산 보유 기준을 초과합니다. (2억 1,550만원 이하)"

    # 자동차 가액 기준 확인 (36,830천 원 이하)
    if own_car and car_price > 36830000:
        return False, "자동차 가액 기준을 초과합니다. (3,683만원 이하)"

    # 3. 공통 조건을 모두 충족한 이후: 일반공급 혹은 특별 공급 조건 확인
    # 3.1 일반공급 조건 확인
    if has_subscription_account:
        subscription_min_date = datetime.now() - timedelta(days=6*30)  # 6개월 전
        if datetime.strptime(subscription_start_date, '%Y-%m-%d') <= subscription_min_date and subscription_payment_count >= 6:
            is_eligible = True
            eligibility_reason = "일반공급 조건을 충족하여 공공임대 자격 요건을 충족합니다."

    # 3.2 특별 공급 조건 확인 (신혼부부, 다자녀, 한부모, 노부모 부양 등)
    current_year = datetime.now().year
    marriage_year = datetime.strptime(marriage_date, '%Y-%m-%d').year if marriage_date else None
    marriage_duration = current_year - marriage_year if marriage_year else None

    if (
        (married and marriage_duration is not None and marriage_duration <= 7) or  # 신혼부부 (혼인 7년 이하)
        (has_children and children_count >= 3) or  # 다자녀 (3명 이상의 자녀)
        (single_parent and has_children and children_count > 0) or  # 한부모 가정
        (birth_date and current_year - datetime.strptime(birth_date, '%Y-%m-%d').year >= 65)  # 노부모 부양 (65세 이상)
    ):
        is_eligible = True
        eligibility_reason = "특별 유형 조건을 충족하여 공공임대 자격 요건을 충족합니다."

    # 최종 자격 판별 결과 반환
    if is_eligible:
        return True, eligibility_reason
    else:
        return False, "공공임대 자격 요건을 충족하지 않습니다."

# 행복주택 유형 판별 함수 (Python 버전)
def is_eligible_for_happy_house(customer_info):
    # 고객 정보
    birth_date = customer_info.get('birthDate')
    enrolled_university = customer_info.get('enrolledUniversity')
    job_seeking = customer_info.get('jobSeeking')
    family_members_count = customer_info.get('familyMembersCount')
    married = customer_info.get('married')
    marriage_date = customer_info.get('marriageDate')
    dual_income = customer_info.get('dualIncome')
    has_children = customer_info.get('hasChildren')
    children_count = customer_info.get('childrenCount')
    youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
    single_parent = customer_info.get('singleParent')
    monthly_income = customer_info.get('monthlyIncome')
    household_monthly_income = customer_info.get('householdMonthlyIncome')
    own_house = customer_info.get('ownHouse')
    assets = customer_info.get('assets')
    own_car = customer_info.get('ownCar')
    car_price = customer_info.get('carPrice')
    has_subscription_account = customer_info.get('hasSubscriptionAccount')
    subscription_start_date = customer_info.get('subscriptionStartDate')
    subscription_payment_count = customer_info.get('subscriptionPaymentCount')
    subscription_payment_amount = customer_info.get('subscriptionPaymentAmount')

    current_year = datetime.now().year
    current_date = datetime.now()

    # 혼인 기간 계산
    marriage_year = datetime.strptime(marriage_date, '%Y-%m-%d').year if marriage_date else None
    marriage_duration = current_year - marriage_year if marriage_year else None

    # 무주택 여부 확인
    if own_house:
        return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

    # 소득 기준 확인 (전년도 도시근로자 가구원수별 월평균 소득 100%)
    income_thresholds = {
        1: 3482964,  # 1인가구 기준
        2: 5415712,  # 2인가구 기준
        3: 7198649,  # 3인가구 기준
        4: 8248467,  # 4인가구 기준
        5: 8775071,  # 5인가구 기준
        6: 9563282,  # 6인가구 기준
        7: 10351493, # 7인가구 기준
        8: 11139704, # 8인가구 기준
    }

    income_threshold = income_thresholds.get(family_members_count, income_thresholds[8])

    # 1인 가구 및 2인 가구 소득 기준 가산 적용
    if family_members_count == 1:
        income_threshold *= 1.2  # 1인 가구는 120%
    elif family_members_count == 2:
        income_threshold *= 1.1  # 2인 가구는 110%

    # 대학생 또는 맞벌이 가구의 경우 소득 기준 120%까지 허용
    if enrolled_university or dual_income:
        income_threshold *= 1.2

    if household_monthly_income > income_threshold:
        return False, "가구 월 평균 소득이 기준을 초과합니다."

    # 자산 보유 기준 확인 (34,500만원 이하)
    if assets > 345000000:
        return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

    # 자동차 가액 기준 확인 (3,708만원 이하)
    if own_car and car_price > 37080000:
        return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

    # 대학생의 경우 자동차 소유 불가
    if enrolled_university and own_car:
        return False, "대학생은 자동차를 소유할 수 없습니다."

    # 세부 특별 유형 확인 (대학생, 청년, 사회초년생, 신혼부부, 한부모가족, 고령자 등)
    birth_year = datetime.strptime(birth_date, '%Y-%m-%d').year
    youngest_child_year = datetime.strptime(youngest_child_birth_date, '%Y-%m-%d').year if youngest_child_birth_date else None

    if (
        (enrolled_university and not married) or  # 대학생 (미혼)
        (job_seeking and not married and 19 <= current_year - birth_year <= 39) or  # 청년 (만 19세 이상 39세 이하)
        (not married and job_seeking and current_year - birth_year <= 39) or  # 사회초년생 (미혼, 5년 이내 직장 경험)
        (married and marriage_duration is not None and marriage_duration <= 7 and has_children and youngest_child_year and current_year - youngest_child_year <= 6) or  # 신혼부부 (혼인 7년 이내, 만 6세 이하 자녀)
        (single_parent and has_children and youngest_child_year and current_year - youngest_child_year <= 6) or  # 한부모 가정 (만 6세 이하 자녀)
        (current_year - birth_year >= 65)  # 고령자 (만 65세 이상)
    ):
        return True, "세부 특별 유형 조건을 충족하여 행복주택 자격 요건을 충족합니다."

    return False, "행복주택 자격 요건을 충족하지 않습니다."

# 행복주택(신혼희망) 유형 판별 함수 (Python 버전)
def is_eligible_for_happy_house_newlywed(customer_info):
    # 고객 정보
    birth_date = customer_info.get('birthDate')
    enrolled_university = customer_info.get('enrolledUniversity')
    job_seeking = customer_info.get('jobSeeking')
    family_members_count = customer_info.get('familyMembersCount')
    married = customer_info.get('married')
    marriage_date = customer_info.get('marriageDate')
    dual_income = customer_info.get('dualIncome')
    has_children = customer_info.get('hasChildren')
    children_count = customer_info.get('childrenCount')
    youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
    single_parent = customer_info.get('singleParent')
    monthly_income = customer_info.get('monthlyIncome')
    household_monthly_income = customer_info.get('householdMonthlyIncome')
    own_house = customer_info.get('ownHouse')
    assets = customer_info.get('assets')
    own_car = customer_info.get('ownCar')
    car_price = customer_info.get('carPrice')
    has_subscription_account = customer_info.get('hasSubscriptionAccount')
    subscription_start_date = customer_info.get('subscriptionStartDate')
    subscription_payment_count = customer_info.get('subscriptionPaymentCount')
    subscription_payment_amount = customer_info.get('subscriptionPaymentAmount')

    current_year = datetime.now().year

    # 무주택 여부 확인
    if own_house:
        return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

    # 혼인 상태 및 혼인 기간 확인 (혼인 중이며 혼인 기간이 7년 이내 또는 예비 신혼부부)
    marriage_duration = None
    if marriage_date:
        marriage_year = datetime.strptime(marriage_date, '%Y-%m-%d').year
        marriage_duration = current_year - marriage_year

    if not (married and marriage_duration is not None and marriage_duration <= 7):
        return False, "혼인 상태가 아니거나 혼인 기간이 7년을 초과하여 신혼희망 자격이 없습니다."

    # 만 6세 이하 자녀 여부 확인
    if has_children:
        youngest_child_year = datetime.strptime(youngest_child_birth_date, '%Y-%m-%d').year
        youngest_child_age = current_year - youngest_child_year
        if youngest_child_age > 6:
            return False, "만 6세 이하 자녀가 없으므로 신혼희망 자격이 없습니다."

    # 가구원 수에 따른 소득 기준 확인 (전년도 도시근로자 가구원수별 월평균 소득 100% 이하)
    income_thresholds = {
        1: 3482964,  # 1인가구 기준
        2: 5415712,  # 2인가구 기준
        3: 7198649,  # 3인가구 기준
        4: 8248467,  # 4인가구 기준
        5: 8775071,  # 5인가구 기준
        6: 9563282,  # 6인가구 기준
        7: 10351493, # 7인가구 기준
        8: 11139704, # 8인가구 기준
    }

    income_threshold = income_thresholds.get(family_members_count, income_thresholds[8])

    # 맞벌이 가구의 경우 소득 기준 120%까지 허용
    if dual_income:
        income_threshold *= 1.2

    if household_monthly_income > income_threshold:
        return False, "가구 월 평균 소득이 기준을 초과합니다."

    # 자산 보유 기준 확인 (34,500만원 이하)
    if assets > 345000000:
        return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

    # 자동차 가액 기준 확인 (3,708만원 이하)
    if own_car and car_price > 37080000:
        return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

    return True, "신혼희망 자격 요건을 충족합니다."

# 장기전세 유형 판별 함수 (Python 버전)
def is_eligible_for_long_term_jeonse(customer_info):
    # 고객 정보
    birth_date = customer_info.get('birthDate')
    enrolled_university = customer_info.get('enrolledUniversity')
    job_seeking = customer_info.get('jobSeeking')
    family_members_count = customer_info.get('familyMembersCount')
    married = customer_info.get('married')
    marriage_date = customer_info.get('marriageDate')
    dual_income = customer_info.get('dualIncome')
    has_children = customer_info.get('hasChildren')
    children_count = customer_info.get('childrenCount')
    youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
    single_parent = customer_info.get('singleParent')
    monthly_income = customer_info.get('monthlyIncome')
    household_monthly_income = customer_info.get('householdMonthlyIncome')
    own_house = customer_info.get('ownHouse')
    assets = customer_info.get('assets')
    own_car = customer_info.get('ownCar')
    car_price = customer_info.get('carPrice')
    has_subscription_account = customer_info.get('hasSubscriptionAccount')
    subscription_start_date = customer_info.get('subscriptionStartDate')
    subscription_payment_count = customer_info.get('subscriptionPaymentCount')
    subscription_payment_amount = customer_info.get('subscriptionPaymentAmount')

    # 무주택 여부 확인
    if own_house:
        return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

    # 소득 기준 확인 (전년도 도시근로자 가구원수별 월평균 소득 100% 이하)
    income_thresholds = {
        1: 3482964,  # 1인가구 기준
        2: 5415712,  # 2인가구 기준
        3: 7198649,  # 3인가구 기준
        4: 8248467,  # 4인가구 기준
        5: 8775071,  # 5인가구 기준
        6: 9563282,  # 6인가구 기준
        7: 10351493, # 7인가구 기준
        8: 11139704, # 8인가구 기준
    }

    income_threshold = income_thresholds.get(family_members_count, income_thresholds[8])

    # 맞벌이 가구의 경우 소득 기준 120%까지 허용
    if dual_income:
        income_threshold *= 1.2

    if household_monthly_income > income_threshold:
        return False, "가구 월 평균 소득이 기준을 초과합니다."

    # 자산 보유 기준 확인
    max_assets = 215500000  # 2억 1,550만원 이하
    if assets > max_assets:
        return False, "총 자산 보유 기준을 초과합니다. (2억 1,550만원 이하)"

    # 자동차 가액 기준 확인 (3,496만원 이하)
    if own_car and car_price > 34960000:
        return False, "자동차 가액 기준을 초과합니다. (3,496만원 이하)"

    # 입주 자격 확인이 모두 통과된 경우
    return True, "장기전세 자격 요건을 충족합니다."

#---------------------------------------------------------------------------------------------------------
# 고객 정보 입력 예시
'''
const customerInfo = {
    // 개인 정보
    birthDate: "1997-10-14", // 생년월일
    enrolledUniversity: false, // 대학생 여부
    jobSeeking: true, // 취업준비생 여부

    // 가족 정보
    familyMembersCount: 4, // 가족 구성원 수
    married: true, // 혼인 여부
    marriageDate: "2019-11-01", // 혼인 신고 또는 혼인 예정일
    dualIncome: false, // 맞벌이 여부
    hasChildren: true, // 자녀 유무
    childrenCount: 2, // 자녀 수
    youngestChildBirthDate: "2023-10-09", // 가장 어린 자녀의 생년월일
    singleParent: false, // 한부모 여부

    // 소득 정보
    monthlyIncome: 1660000, // 월 평균 소득 (단위: 원)
    householdMonthlyIncome: 4160000, // 가구 월 평균 소득 (단위: 원)
    ownHouse: false, // 주택 소유 여부

    // 자산 정보
    assets: 60000000, // 총 자산 (단위: 원)
    ownCar: true, // 자동차 소유 여부
    carPrice: 30000000, // 자동차 가격 (단위: 원)

    // 청약 통장 정보
    hasSubscriptionAccount: true, // 청약 통장 소유 여부
    subscriptionStartDate: "2020-10-09", // 청약 통장 가입 일자
    subscriptionPaymentCount: 30, // 청약 통장 납입 횟수
    subscriptionPaymentAmount: 10000000, // 청약 통장 납입 금액 (단위: 원)

    // 추가 필터 조건
    region: "서울특별시", // 원하는 지역
    status: "전체", // 공고 상태 (공고중, 접수중, 접수마감, 정정공고중)
    startDate: "2023.09.08", // 게시일 시작
    endDate: "2024.9.08", // 게시일 종료
};
'''
#---------------------------------------------------------------------------------------------------------
# 프론트에서 고객 정보를 위의 형식으로 JSON으로 받아온다고 가정
# 고객 정보 JSON 파일 경로

customer_info_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '고객정보.json')  # 받아올 고객정보 디렉토리

# 고객 정보를 JSON 파일에서 읽어오는 함수
def read_customer_info_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
            return json.loads(data)
    except Exception as err:
        print("고객 정보 JSON 파일을 읽는 중 오류가 발생했습니다:", err)
        return None

# 고객 정보 읽어오기
customer_info = read_customer_info_from_file(customer_info_file_path)

#---------------------------------------------------------------------------------------------------------
# 고객 정보 바탕으로 유형 판별 

'''
통합공공임대
통합공공임대(신혼희망)
국민임대
공공임대
행복주택
행복주택(신혼희망)
장기전세
'''

# 공공임대 유형 자격 여부 판단 함수 호출
def run_eligibility_checks(customer_info):
    print("----------------------------------------------------------")
    print("통합공공임대")
    integrated_public_eligible, integrated_public_message = is_eligible_for_total_public_rental(customer_info)
    print(integrated_public_message)
    print("----------------------------------------------------------\n")

    print("----------------------------------------------------------")
    print("통합공공임대(신혼희망)")
    integrated_public_eligible_newly_wed, integrated_public_message_newly_wed = is_eligible_for_total_public_rental_newlywed(customer_info)
    print(integrated_public_message_newly_wed)
    print("----------------------------------------------------------\n")

    print("----------------------------------------------------------")
    print("국민임대")
    national_eligible, national_message = is_eligible_for_national_rental(customer_info)
    print(national_message)
    print("----------------------------------------------------------\n")

    print("----------------------------------------------------------")
    print("공공임대")
    public_eligible, public_message = is_eligible_for_public_rental(customer_info)
    print(public_message)
    print("----------------------------------------------------------\n")

    print("----------------------------------------------------------")
    print("행복주택")
    happy_house_eligible, happy_house_message = is_eligible_for_happy_house(customer_info)
    print(happy_house_message)
    print("----------------------------------------------------------\n")

    print("----------------------------------------------------------")
    print("행복주택(신혼희망)")
    happy_eligible_newly_wed, happy_message_newly_wed = is_eligible_for_happy_house_newlywed(customer_info)
    print(happy_message_newly_wed)
    print("----------------------------------------------------------\n")

    print("----------------------------------------------------------")
    print("장기전세")
    long_term_jeonse_eligible, long_term_jeonse_message = is_eligible_for_long_term_jeonse(customer_info)
    print(long_term_jeonse_message)
    print("----------------------------------------------------------\n")

    return {
        'integrated_public_eligible': integrated_public_eligible,
        'integrated_public_eligible_newly_wed': integrated_public_eligible_newly_wed,
        'national_eligible': national_eligible,
        'public_eligible': public_eligible,
        'happy_house_eligible': happy_house_eligible,
        'happy_eligible_newly_wed': happy_eligible_newly_wed,
        'long_term_jeonse_eligible': long_term_jeonse_eligible,
    }

# 자격 여부 확인 및 최종 결과 출력
eligible_rental_types = []

eligibility_results = run_eligibility_checks(customer_info)

if eligibility_results['integrated_public_eligible']:
    eligible_rental_types.append("통합공공임대")
if eligibility_results['integrated_public_eligible_newly_wed']:
    eligible_rental_types.append("통합공공임대(신혼희망)")
if eligibility_results['national_eligible']:
    eligible_rental_types.append("국민임대")
if eligibility_results['public_eligible']:
    eligible_rental_types.append("공공임대")
if eligibility_results['happy_house_eligible']:
    eligible_rental_types.append("행복주택")
if eligibility_results['happy_eligible_newly_wed']:
    eligible_rental_types.append("행복주택(신혼희망)")
if eligibility_results['long_term_jeonse_eligible']:
    eligible_rental_types.append("장기전세")

# 최종 결과 출력
if eligible_rental_types:
    print("고객님께 적합한 임대 유형은 다음과 같습니다:")
    for rental_type in eligible_rental_types:
        print(f"- {rental_type}")
else:
    print("고객님께 적합한 임대 유형이 없습니다.")

#---------------------------------------------------------------------------------------------------------
# CSV 파일에서 공고 데이터를 필터링하는 함수
def filter_announcements_from_csv(csv_file_path, criteria, rental_types):
    filtered_announcements = []

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # 지역 필터
                region_match = criteria['region'] == "전국" or row['지역'] == criteria['region']

                # 상태 필터
                status_match = criteria['status'] == "전체" or row['공고상태'] == criteria['status']

                # 게시일 필터
                post_date = datetime.strptime(row['공고게시일'], '%Y.%m.%d')
                start_date = datetime.strptime(criteria['startDate'], '%Y.%m.%d')
                end_date = datetime.strptime(criteria['endDate'], '%Y.%m.%d')
                date_match = start_date <= post_date <= end_date

                # 공고 유형 필터
                type_match = len(rental_types) == 0 or row['주택유형'] in rental_types

                # 모든 필터가 만족하는 경우 해당 공고를 필터링된 배열에 추가
                if region_match and status_match and date_match and type_match:
                    filtered_announcements.append(row)

        # 필터링된 결과 JSON으로 출력 및 저장
        if filtered_announcements:
            print(f"고객님께 적합한 공고가 총 {len(filtered_announcements)}개 있습니다.")

            # JSON 파일로 저장
            output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '최종결정된공고리스트_py.json')
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(filtered_announcements, output_file, ensure_ascii=False, indent=2)
            print("필터링된 공고 목록이 '최종결정된공고리스트.json'에 저장되었습니다.")
        else:
            print("고객님께 적합한 공고가 없습니다.")

    except Exception as err:
        print("CSV 파일을 읽는 중 오류가 발생했습니다:", err)

# CSV 파일 경로 설정
csv_file_path = r'C:\Users\LG\Desktop\VS 공공데이터OpenAPI\collect_DATA\중복제거_공고목록.csv'

# 필터링 함수 호출
filter_announcements_from_csv(csv_file_path, customer_info, eligible_rental_types)

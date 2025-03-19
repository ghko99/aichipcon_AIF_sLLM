import os
import csv
import json
from datetime import datetime, timedelta

def search(customer_info):
    print("Search function called.")

    '''
    고객 정보를 받아서 적합한 임대 유형을 판단하고,
    해당 임대 유형에 맞는 공고를 CSV 파일에서 필터링하여 반환하는 함수입니다.
    '''
    if customer_info is None:
        customer_info = {}
        print("Customer info is None. Initialized to empty dictionary.")

    try:
        # marriageDate 처리
        marriage_date = customer_info.get('marriageDate')
        if marriage_date:
            try:
                marriage_date_obj = datetime.strptime(marriage_date, '%Y-%m-%d')
            except ValueError:
                print("Invalid marriageDate format. Setting to None.")
                marriage_date_obj = None
        else:
            marriage_date_obj = None

        # youngestChildBirthDate 처리
        youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
        if youngest_child_birth_date:
            try:
                youngest_child_birth_date_obj = datetime.strptime(youngest_child_birth_date, '%Y-%m-%d')
            except ValueError:
                print("Invalid youngestChildBirthDate format. Setting to None.")
                youngest_child_birth_date_obj = None
        else:
            youngest_child_birth_date_obj = None
            print("Processed dates successfully.")

    except Exception as e:
        print("Error in search function during date processing:", e)
        raise

    # 통합공공임대 유형 판별 함수
    def is_eligible_for_total_public_rental(customer_info):
        try:
            # 고객 정보
            family_members_count = customer_info.get('familyMembersCount', 0)
            household_monthly_income = customer_info.get('householdMonthlyIncome', 0)
            own_house = customer_info.get('ownHouse', False)
            assets = customer_info.get('assets', 0)
            own_car = customer_info.get('ownCar', False)
            car_price = customer_info.get('carPrice', 0)

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

            median_income_threshold = median_income_thresholds.get(family_members_count, 
                median_income_thresholds[8] + (family_members_count - 8) * 879534)

            if household_monthly_income > median_income_threshold * 1.5:
                return False, "가구 월 평균 소득이 기준 중위소득의 150%를 초과합니다."

            # 총자산 보유 기준 확인 (34,500만원 이하)
            if assets > 345000000:
                return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

            # 자동차 가액 기준 확인 (3,708만원 이하)
            if own_car and car_price > 37080000:
                return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

            return True, "통합공공임대 자격 요건을 충족합니다."
        except Exception as e:
            print("Error in is_eligible_for_total_public_rental:", e)
            return False, "오류로 인해 자격 판별에 실패했습니다."

    # 통합공공임대(신혼희망) 유형 판별 함수
    def is_eligible_for_total_public_rental_newlywed(customer_info):
        try:
            # 고객 정보
            family_members_count = customer_info.get('familyMembersCount', 0)
            married = customer_info.get('married', False)
            marriage_date = customer_info.get('marriageDate')
            has_children = customer_info.get('hasChildren', False)
            youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
            household_monthly_income = customer_info.get('householdMonthlyIncome', 0)
            own_house = customer_info.get('ownHouse', False)
            assets = customer_info.get('assets', 0)
            own_car = customer_info.get('ownCar', False)
            car_price = customer_info.get('carPrice', 0)

            # 무주택 여부 확인
            if own_house:
                return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

            current_date = datetime.now()
            marriage_date_obj = None
            marriage_duration = None
            if marriage_date:
                try:
                    marriage_date_obj = datetime.strptime(marriage_date, '%Y-%m-%d')
                    marriage_duration = current_date.year - marriage_date_obj.year
                except ValueError:
                    print("Invalid marriageDate format. Setting marriage_duration to None.")

            # 혼인 상태 및 기간 조건 확인
            if not ((married and marriage_duration is not None and marriage_duration <= 7) or 
                    (not married and marriage_date_obj and marriage_date_obj > current_date)):
                return False, "혼인 상태가 아니거나 혼인 기간이 7년을 초과하여 신혼부부 자격이 없습니다."

            # 만 6세 이하 자녀 여부 확인
            if has_children and youngest_child_birth_date:
                try:
                    youngest_child_year = youngest_child_birth_date_obj.year
                    youngest_child_age = current_date.year - youngest_child_year
                    if youngest_child_age > 6:
                        return False, "만 6세 이하 자녀가 없으므로 신혼부부 자격이 없습니다."
                except Exception:
                    print("Error processing youngest_child_birth_date_obj.")
                    return False, "자녀 정보 처리 오류로 신혼부부 자격을 판단할 수 없습니다."

            # 가구 월 평균 소득 기준 확인
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

            median_income_threshold = median_income_thresholds.get(family_members_count, 
                median_income_thresholds[8] + (family_members_count - 8) * 879534)

            if household_monthly_income > median_income_threshold:
                return False, "가구 월 평균 소득이 기준 중위소득을 초과합니다."

            # 총자산 보유 기준 확인 (34,500만원 이하)
            if assets > 345000000:
                return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

            # 자동차 가액 기준 확인 (3,708만원 이하)
            if own_car and car_price > 37080000:
                return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

            return True, "통합공공임대(신혼희망) 자격 요건을 충족합니다."
        except Exception as e:
            print("Error in is_eligible_for_total_public_rental_newlywed:", e)
            return False, "오류로 인해 자격 판별에 실패했습니다."

    # 국민임대 유형 판별 함수
    def is_eligible_for_national_rental(customer_info):
        try:
            # 고객 정보
            family_members_count = customer_info.get('familyMembersCount', 0)
            household_monthly_income = customer_info.get('householdMonthlyIncome', 0)
            own_house = customer_info.get('ownHouse', False)
            assets = customer_info.get('assets', 0)
            own_car = customer_info.get('ownCar', False)
            car_price = customer_info.get('carPrice', 0)

            # 무주택 여부 확인
            if own_house:
                return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

            # 가구 월 평균 소득 기준 확인
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

            income_threshold = income_thresholds.get(family_members_count, 
                income_thresholds[8] + (family_members_count - 8) * 879534)

            if household_monthly_income > income_threshold:
                return False, "가구 월 평균 소득이 국민임대 기준 소득을 초과합니다."

            # 총자산 보유 기준 확인 (34,500만원 이하)
            if assets > 345000000:
                return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

            # 자동차 가액 기준 확인 (3,708만원 이하)
            if own_car and car_price > 37080000:
                return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

            return True, "국민임대 자격 요건을 충족합니다."
        except Exception as e:
            print("Error in is_eligible_for_national_rental:", e)
            return False, "오류로 인해 자격 판별에 실패했습니다."

    # 공공임대 유형 판별 함수
    def is_eligible_for_public_rental(customer_info):
        try:
            # 고객 정보
            family_members_count = customer_info.get('familyMembersCount', 0)
            married = customer_info.get('married', False)
            marriage_date = customer_info.get('marriageDate')
            dual_income = customer_info.get('dualIncome', False)
            has_children = customer_info.get('hasChildren', False)
            children_count = customer_info.get('childrenCount', 0)
            single_parent = customer_info.get('singleParent', False)
            monthly_income = customer_info.get('monthlyIncome', 0)
            household_monthly_income = customer_info.get('householdMonthlyIncome', 0)
            own_house = customer_info.get('ownHouse', False)
            assets = customer_info.get('assets', 0)
            own_car = customer_info.get('ownCar', False)
            car_price = customer_info.get('carPrice', 0)
            has_subscription_account = customer_info.get('hasSubscriptionAccount', False)

            is_eligible = False
            eligibility_reason = ""

            # 1. 공통 조건: 무주택 여부 확인
            if own_house:
                return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

            # 2. 공통 자격 조건 확인 (소득, 자산, 자동차 기준)
            # 소득 기준 확인 (전년도 도시근로자 가구원수별 월평균 소득 100% 이하)
            income_thresholds = {
                1: 3482964,  # 1인가구
                2: 5415712,  # 2인가구
                3: 7198649,  # 3인가구
                4: 8248467,  # 4인가구
                5: 8775071,  # 5인가구
                6: 9563282,  # 6인가구
                7: 10351493,  # 7인가구
                8: 11139704,  # 8인가구
            }

            income_threshold = income_thresholds.get(family_members_count, 
                income_thresholds[8])

            # 맞벌이 가구의 경우 소득 기준 120%까지 허용
            if dual_income:
                income_threshold *= 1.2

            if household_monthly_income > income_threshold:
                return False, "가구 월 평균 소득이 기준을 초과합니다."

            # 자산 보유 기준 확인 (부동산 2억 1,550만원 이하)
            if assets > 215500000:
                return False, "총 자산 보유 기준을 초과합니다. (2억 1,550만원 이하)"

            # 자동차 가액 기준 확인 (36,830천 원 이하)
            if own_car and car_price > 36830000:
                return False, "자동차 가액 기준을 초과합니다. (3,683만원 이하)"

            # 3. 공통 조건을 모두 충족한 이후: 일반공급 혹은 특별 공급 조건 확인
            # 3.1 일반공급 조건 확인
            if has_subscription_account:
                is_eligible = True
                eligibility_reason = "일반공급 조건을 충족하여 공공임대 자격 요건을 충족합니다."

            # 3.2 특별 공급 조건 확인 (신혼부부, 다자녀, 한부모 등)
            current_year = datetime.now().year
            marriage_year = None
            marriage_duration = None
            if marriage_date:
                try:
                    marriage_year = datetime.strptime(marriage_date, '%Y-%m-%d').year
                    marriage_duration = current_year - marriage_year
                except ValueError:
                    print("Invalid marriageDate format. Setting marriage_duration to None.")

            if (
                (married and marriage_duration is not None and marriage_duration <= 7) or  # 신혼부부 (혼인 7년 이하)
                (has_children and children_count >= 3) or  # 다자녀 (3명 이상의 자녀)
                (single_parent)   # 한부모 가정
            ):
                is_eligible = True
                eligibility_reason = "특별 유형 조건을 충족하여 공공임대 자격 요건을 충족합니다."

            # 최종 자격 판별 결과 반환
            if is_eligible:
                return True, eligibility_reason
            else:
                return False, "공공임대 자격 요건을 충족하지 않습니다."
        except Exception as e:
            print("Error in is_eligible_for_public_rental:", e)
            return False, "오류로 인해 자격 판별에 실패했습니다."

    # 행복주택 유형 판별 함수
    def is_eligible_for_happy_house(customer_info):
        try:
            # 고객 정보
            age = customer_info.get('age')
            birth_date = customer_info.get('birthDate')
            enrolled_university = customer_info.get('enrolledUniversity', False)
            job_seeking = customer_info.get('jobSeeking', False)
            family_members_count = customer_info.get('familyMembersCount', 0)
            married = customer_info.get('married', False)
            marriage_date = customer_info.get('marriageDate')
            dual_income = customer_info.get('dualIncome', False)
            has_children = customer_info.get('hasChildren', False)
            children_count = customer_info.get('childrenCount', 0)
            youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
            single_parent = customer_info.get('singleParent', False)
            monthly_income = customer_info.get('monthlyIncome', 0)
            household_monthly_income = customer_info.get('householdMonthlyIncome', 0)
            own_house = customer_info.get('ownHouse', False)
            assets = customer_info.get('assets', 0)
            own_car = customer_info.get('ownCar', False)
            car_price = customer_info.get('carPrice', 0)

            current_year = datetime.now().year
            current_date = datetime.now()

            # 혼인 기간 계산
            marriage_year = None
            marriage_duration = None
            if marriage_date:
                try:
                    marriage_year = datetime.strptime(marriage_date, '%Y-%m-%d').year
                    marriage_duration = current_year - marriage_year
                except ValueError:
                    print("Invalid marriageDate format. Setting marriage_duration to None.")

            # 무주택 여부 확인
            if own_house:
                return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

            # 소득 기준 확인
            income_thresholds = {
                1: 3482964,  # 1인가구
                2: 5415712,  # 2인가구
                3: 7198649,  # 3인가구
                4: 8248467,  # 4인가구
                5: 8775071,  # 5인가구
                6: 9563282,  # 6인가구
                7: 10351493,  # 7인가구
                8: 11139704,  # 8인가구
            }

            income_threshold = income_thresholds.get(family_members_count, 
                income_thresholds[8])

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

            # 총자산 보유 기준 확인 (34,500만원 이하)
            if assets > 345000000:
                return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

            # 자동차 가액 기준 확인 (3,708만원 이하)
            if own_car and car_price > 37080000:
                return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

            # 대학생의 경우 자동차 소유 불가
            if enrolled_university and own_car:
                return False, "대학생은 자동차를 소유할 수 없습니다."

            # 세부 특별 유형 확인
            birth_year = current_year - age if age else None
            youngest_child_year = None
            youngest_child_age = None
            if youngest_child_birth_date:
                try:
                    youngest_child_year = youngest_child_birth_date_obj.year
                    youngest_child_age = current_year - youngest_child_year
                except Exception:
                    print("Error processing youngest_child_birth_date_obj.")

            if (
                (enrolled_university and not married) or  # 대학생 (미혼)
                (job_seeking and not married and birth_year and 19 <= current_year - birth_year <= 39) or  # 청년
                (not married and job_seeking and birth_year and current_year - birth_year <= 39) or  # 사회초년생
                (married and marriage_duration is not None and marriage_duration <= 7 and has_children and youngest_child_year and youngest_child_age <= 6) or  # 신혼부부
                (single_parent) or  # 한부모 가정
                (birth_year and current_year - birth_year >= 65)  # 고령자
            ):
                return True, "세부 특별 유형 조건을 충족하여 행복주택 자격 요건을 충족합니다."

            return False, "행복주택 자격 요건을 충족하지 않습니다."
        except Exception as e:
            print("Error in is_eligible_for_happy_house:", e)
            return False, "오류로 인해 자격 판별에 실패했습니다."

    # 행복주택(신혼희망) 유형 판별 함수
    def is_eligible_for_happy_house_newlywed(customer_info):
        try:
            # 고객 정보
            family_members_count = customer_info.get('familyMembersCount', 0)
            married = customer_info.get('married', False)
            marriage_date = customer_info.get('marriageDate')
            dual_income = customer_info.get('dualIncome', False)
            has_children = customer_info.get('hasChildren', False)
            youngest_child_birth_date = customer_info.get('youngestChildBirthDate')
            household_monthly_income = customer_info.get('householdMonthlyIncome', 0)
            own_house = customer_info.get('ownHouse', False)
            assets = customer_info.get('assets', 0)
            own_car = customer_info.get('ownCar', False)
            car_price = customer_info.get('carPrice', 0)

            current_year = datetime.now().year

            # 무주택 여부 확인
            if own_house:
                return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

            # 혼인 상태 및 혼인 기간 확인
            marriage_duration = None
            if marriage_date:
                try:
                    marriage_year = datetime.strptime(marriage_date, '%Y-%m-%d').year
                    marriage_duration = current_year - marriage_year
                except ValueError:
                    print("Invalid marriageDate format. Setting marriage_duration to None.")

            if not (married and marriage_duration is not None and marriage_duration <= 7):
                return False, "혼인 상태가 아니거나 혼인 기간이 7년을 초과하여 신혼희망 자격이 없습니다."

            # 만 6세 이하 자녀 여부 확인
            if has_children and youngest_child_birth_date:
                try:
                    youngest_child_year = youngest_child_birth_date_obj.year
                    youngest_child_age = current_year - youngest_child_year
                    if youngest_child_age > 6:
                        return False, "만 6세 이하 자녀가 없으므로 신혼희망 자격이 없습니다."
                except Exception:
                    print("Error processing youngest_child_birth_date_obj.")
                    return False, "자녀 정보 처리 오류로 신혼희망 자격을 판단할 수 없습니다."

            # 가구원 수에 따른 소득 기준 확인
            income_thresholds = {
                1: 3482964,  # 1인가구
                2: 5415712,  # 2인가구
                3: 7198649,  # 3인가구
                4: 8248467,  # 4인가구
                5: 8775071,  # 5인가구
                6: 9563282,  # 6인가구
                7: 10351493,  # 7인가구
                8: 11139704,  # 8인가구
            }

            income_threshold = income_thresholds.get(family_members_count, 
                income_thresholds[8])

            # 맞벌이 가구의 경우 소득 기준 120%까지 허용
            if dual_income:
                income_threshold *= 1.2

            if household_monthly_income > income_threshold:
                return False, "가구 월 평균 소득이 기준을 초과합니다."

            # 총자산 보유 기준 확인 (34,500만원 이하)
            if assets > 345000000:
                return False, "총 자산 보유 기준을 초과합니다. (34,500만원 이하)"

            # 자동차 가액 기준 확인 (3,708만원 이하)
            if own_car and car_price > 37080000:
                return False, "자동차 가액 기준을 초과합니다. (3,708만원 이하)"

            return True, "신혼희망 자격 요건을 충족합니다."
        except Exception as e:
            print("Error in is_eligible_for_happy_house_newlywed:", e)
            return False, "오류로 인해 자격 판별에 실패했습니다."

    # 장기전세 유형 판별 함수
    def is_eligible_for_long_term_jeonse(customer_info):
        try:
            # 고객 정보
            family_members_count = customer_info.get('familyMembersCount', 0)
            dual_income = customer_info.get('dualIncome', False)
            household_monthly_income = customer_info.get('householdMonthlyIncome', 0)
            own_house = customer_info.get('ownHouse', False)
            assets = customer_info.get('assets', 0)
            own_car = customer_info.get('ownCar', False)
            car_price = customer_info.get('carPrice', 0)

            # 무주택 여부 확인
            if own_house:
                return False, "주택을 소유하고 있으므로 무주택세대구성원 자격이 없습니다."

            # 소득 기준 확인 (전년도 도시근로자 가구원수별 월평균 소득 100% 이하)
            income_thresholds = {
                1: 3482964,  # 1인가구
                2: 5415712,  # 2인가구
                3: 7198649,  # 3인가구
                4: 8248467,  # 4인가구
                5: 8775071,  # 5인가구
                6: 9563282,  # 6인가구
                7: 10351493,  # 7인가구
                8: 11139704,  # 8인가구
            }

            income_threshold = income_thresholds.get(family_members_count, 
                income_thresholds[8])

            # 맞벌이 가구의 경우 소득 기준 120%까지 허용
            if dual_income:
                income_threshold *= 1.2

            if household_monthly_income > income_threshold:
                return False, "가구 월 평균 소득이 기준을 초과합니다."

            # 자산 보유 기준 확인 (2억 1,550만원 이하)
            max_assets = 215500000  # 2억 1,550만원 이하
            if assets > max_assets:
                return False, "총 자산 보유 기준을 초과합니다. (2억 1,550만원 이하)"

            # 자동차 가액 기준 확인 (3,496만원 이하)
            if own_car and car_price > 34960000:
                return False, "자동차 가액 기준을 초과합니다. (3,496만원 이하)"

            # 입주 자격 확인이 모두 통과된 경우
            return True, "장기전세 자격 요건을 충족합니다."
        except Exception as e:
            print("Error in is_eligible_for_long_term_jeonse:", e)
            return False, "오류로 인해 자격 판별에 실패했습니다."

    # 공공임대 유형 자격 여부 판단 함수 호출
    def run_eligibility_checks(customer_info):
        try:
            integrated_public_eligible, _ = is_eligible_for_total_public_rental(customer_info)
            integrated_public_eligible_newly_wed, _ = is_eligible_for_total_public_rental_newlywed(customer_info)
            national_eligible, _ = is_eligible_for_national_rental(customer_info)
            public_eligible, _ = is_eligible_for_public_rental(customer_info)
            happy_house_eligible, _ = is_eligible_for_happy_house(customer_info)
            happy_eligible_newly_wed, _ = is_eligible_for_happy_house_newlywed(customer_info)
            long_term_jeonse_eligible, _ = is_eligible_for_long_term_jeonse(customer_info)

            return {
                'integrated_public_eligible': integrated_public_eligible,
                'integrated_public_eligible_newly_wed': integrated_public_eligible_newly_wed,
                'national_eligible': national_eligible,
                'public_eligible': public_eligible,
                'happy_house_eligible': happy_house_eligible,
                'happy_eligible_newly_wed': happy_eligible_newly_wed,
                'long_term_jeonse_eligible': long_term_jeonse_eligible,
            }
        except Exception as e:
            print("Error in run_eligibility_checks:", e)
            return {
                'integrated_public_eligible': False,
                'integrated_public_eligible_newly_wed': False,
                'national_eligible': False,
                'public_eligible': False,
                'happy_house_eligible': False,
                'happy_eligible_newly_wed': False,
                'long_term_jeonse_eligible': False,
            }

    # 자격 여부 확인 및 적합한 임대 유형 결정
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

    # CSV 파일에서 공고 데이터를 필터링하는 함수
    def filter_announcements_from_csv(criteria, rental_types):
        # CSV 파일 경로 설정
        csv_file_path = r'/home/guest/main/backend/search/final_data.csv'

        filtered_announcements = []

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    # 번호를 int로 변환 (소수점 제거 처리)
                    try:
                        row['번호'] = int(float(row['번호']))
                    except (ValueError, KeyError):
                        continue

                    # 지역 필터
                    region = criteria.get('region', "전국")
                    region_match = region == "전국" or row.get('지역') == region

                    # 상태 필터
                    status = criteria.get('status', "공고중")
                    status_match = status == "공고중" or row.get('공고상태') == status

                    # 게시일 필터
                    try:
                        post_date_str = row.get('공고게시일')
                        if not post_date_str:
                            continue
                        post_date = datetime.strptime(post_date_str, '%Y.%m.%d')
                        start_date_str = criteria.get('startDate', '1900.01.01')
                        end_date_str = criteria.get('endDate', '9999.12.31')
                        start_date = datetime.strptime(start_date_str, '%Y.%m.%d')
                        end_date = datetime.strptime(end_date_str, '%Y.%m.%d')
                        date_match = start_date <= post_date <= end_date
                    except Exception:
                        continue

                    # 공고 유형 필터
                    type_match = len(rental_types) == 0 or row.get('주택유형') in rental_types

                    # 모든 필터가 만족하는 경우 해당 공고를 필터링된 배열에 추가
                    if region_match and status_match and date_match and type_match:
                        filtered_announcements.append(row)

                if filtered_announcements:
                    print("고객님께 적합한 공고가 총 {}개 있습니다.".format(len(filtered_announcements)))
                    # json으로 저장
                    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                                   'announcements.json')
                    try:
                        with open(output_file_path, 'w', encoding='utf-8') as output_file:
                            json.dump(filtered_announcements, output_file, ensure_ascii=False, indent=2)
                    except Exception as e:
                        print("JSON 파일 저장 중 오류가 발생했습니다:", e)
                else:
                    print("고객님께 적합한 공고가 없습니다.")

            return filtered_announcements

        except FileNotFoundError:
            print("CSV 파일을 찾을 수 없습니다:", csv_file_path)
            return []
        except Exception as err:
            print("CSV 파일을 읽는 중 오류가 발생했습니다:", err)
            return []

    # 필터링 함수 호출
    filtered_announcements = filter_announcements_from_csv(customer_info, eligible_rental_types)

    # 최종 결과 반환
    return filtered_announcements

if __name__ == "__main__":
    customer_info_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '고객정보.json')  # 받아올 고객정보 디렉토리

    # 고객 정보를 JSON 파일에서 읽어오는 함수
    def read_customer_info_from_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.read()
                return json.loads(data)
        except FileNotFoundError:
            print("고객 정보 JSON 파일을 찾을 수 없습니다:", file_path)
            return None
        except json.JSONDecodeError:
            print("고객 정보 JSON 파일의 형식이 올바르지 않습니다:", file_path)
            return None
        except Exception as err:
            print("고객 정보 JSON 파일을 읽는 중 오류가 발생했습니다:", err)
            return None

    # 고객 정보 읽어오기
    customer_info = read_customer_info_from_file(customer_info_file_path)
    # 함수 호출
    filtered_announcements = search(customer_info)

    # 결과 출력
    if filtered_announcements:
        print("고객님께 적합한 공고가 총 {}개 있습니다.".format(len(filtered_announcements)))
        for announcement in filtered_announcements:
            # print(announcement)
            pass
    else:
        print("고객님께 적합한 공고가 없습니다.")

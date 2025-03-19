import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

interface DetailedFiltersProps {
  filters: any
  setFilters: (filters: any) => void
}

export function DetailedFilters({ filters, setFilters }: DetailedFiltersProps) {
  const handleChange = (key: string, value: any) => {
    setFilters((prev: any) => ({ ...prev, [key]: value }))
  }

  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="space-y-2">
        <Label htmlFor="age">나이</Label>
        <Input
          id="age"
          type="number"
          value={filters.age || ''}
          onChange={(e) => handleChange('age', parseInt(e.target.value))}
        />
      </div>
      <div className="flex items-center space-x-2">
        <Checkbox
          id="enrolledUniversity"
          checked={filters.enrolledUniversity}
          onCheckedChange={(checked) => handleChange('enrolledUniversity', checked)}
        />
        <Label htmlFor="enrolledUniversity">대학 재학 여부</Label>
      </div>
      <div className="flex items-center space-x-2">
        <Checkbox
          id="jobSeeking"
          checked={filters.jobSeeking}
          onCheckedChange={(checked) => handleChange('jobSeeking', checked)}
        />
        <Label htmlFor="jobSeeking">구직자 여부</Label>
      </div>
      <div className="space-y-2">
        <Label htmlFor="familyMembersCount">가족 구성원 수</Label>
        <Input
          id="familyMembersCount"
          type="number"
          value={filters.familyMembersCount || ''}
          onChange={(e) => handleChange('familyMembersCount', parseInt(e.target.value))}
        />
      </div>
      <div className="flex items-center space-x-2">
        <Checkbox
          id="married"
          checked={filters.married}
          onCheckedChange={(checked) => handleChange('married', checked)}
        />
        <Label htmlFor="married">기혼 여부</Label>
      </div>
      {filters.married && (
        <>
          <div className="space-y-2">
            <Label htmlFor="marriageDate">결혼일</Label>
            <Input
              id="marriageDate"
              type="date"
              value={filters.marriageDate || ''}
              onChange={(e) => handleChange('marriageDate', e.target.value)}
            />
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox
              id="dualIncome"
              checked={filters.dualIncome}
              onCheckedChange={(checked) => handleChange('dualIncome', checked)}
            />
            <Label htmlFor="dualIncome">맞벌이 여부</Label>
          </div>
        </>
      )}
      <div className="flex items-center space-x-2">
        <Checkbox
          id="hasChildren"
          checked={filters.hasChildren}
          onCheckedChange={(checked) => handleChange('hasChildren', checked)}
        />
        <Label htmlFor="hasChildren">자녀 유무</Label>
      </div>
      {filters.hasChildren && (
        <>
          <div className="space-y-2">
            <Label htmlFor="childrenCount">자녀 수</Label>
            <Input
              id="childrenCount"
              type="number"
              value={filters.childrenCount || ''}
              onChange={(e) => handleChange('childrenCount', parseInt(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="youngestChildBirthDate">막내 자녀 생년월일</Label>
            <Input
              id="youngestChildBirthDate"
              type="date"
              value={filters.youngestChildBirthDate || ''}
              onChange={(e) => handleChange('youngestChildBirthDate', e.target.value)}
            />
          </div>
        </>
      )}
      <div className="flex items-center space-x-2">
        <Checkbox
          id="singleParent"
          checked={filters.singleParent}
          onCheckedChange={(checked) => handleChange('singleParent', checked)}
        />
        <Label htmlFor="singleParent">한부모 가정 여부</Label>
      </div>
      <div className="space-y-2">
        <Label htmlFor="monthlyIncome">월 소득</Label>
        <Input
          id="monthlyIncome"
          type="number"
          value={filters.monthlyIncome || ''}
          onChange={(e) => handleChange('monthlyIncome', parseInt(e.target.value))}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="householdMonthlyIncome">가구 월 소득</Label>
        <Input
          id="householdMonthlyIncome"
          type="number"
          value={filters.householdMonthlyIncome || ''}
          onChange={(e) => handleChange('householdMonthlyIncome', parseInt(e.target.value))}
        />
      </div>
      <div className="flex items-center space-x-2">
        <Checkbox
          id="ownHouse"
          checked={filters.ownHouse}
          onCheckedChange={(checked) => handleChange('ownHouse', checked)}
        />
        <Label htmlFor="ownHouse">주택 소유 여부</Label>
      </div>
      <div className="space-y-2">
        <Label htmlFor="assets">자산</Label>
        <Input
          id="assets"
          type="number"
          value={filters.assets || ''}
          onChange={(e) => handleChange('assets', parseInt(e.target.value))}
        />
      </div>
      <div className="flex items-center space-x-2">
        <Checkbox
          id="ownCar"
          checked={filters.ownCar}
          onCheckedChange={(checked) => handleChange('ownCar', checked)}
        />
        <Label htmlFor="ownCar">자동차 소유 여부</Label>
      </div>
      {filters.ownCar && (
        <div className="space-y-2">
          <Label htmlFor="carPrice">자동차 가격</Label>
          <Input
            id="carPrice"
            type="number"
            value={filters.carPrice || ''}
            onChange={(e) => handleChange('carPrice', parseInt(e.target.value))}
          />
        </div>
      )}
      <div className="flex items-center space-x-2">
        <Checkbox
          id="hasSubscriptionAccount"
          checked={filters.hasSubscriptionAccount}
          onCheckedChange={(checked) => handleChange('hasSubscriptionAccount', checked)}
        />
        <Label htmlFor="hasSubscriptionAccount">청약통장 보유 여부</Label>
      </div>
    </div>
  )
}


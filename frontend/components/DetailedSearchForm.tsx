import React from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface DetailedSearchFormProps {
  detailedSearch: any;
  handleDetailedSearchChange: (field: string, value: any) => void;
  saveDetailedSearch: () => void;
}

export function DetailedSearchForm({ detailedSearch, handleDetailedSearchChange, saveDetailedSearch }: DetailedSearchFormProps) {
  return (
    <div className="space-y-4 border-t pt-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="age">나이</Label>
          <Input
            id="age"
            type="number"
            value={detailedSearch.age}
            onChange={(e) => handleDetailedSearchChange('age', parseInt(e.target.value))}
          />
        </div>
        <div className="flex items-center space-x-2">
          <Checkbox
            id="enrolledUniversity"
            checked={detailedSearch.enrolledUniversity}
            onCheckedChange={(checked) => handleDetailedSearchChange('enrolledUniversity', checked)}
          />
          <Label htmlFor="enrolledUniversity">대학생 여부</Label>
        </div>
        <div className="flex items-center space-x-2">
          <Checkbox
            id="jobSeeking"
            checked={detailedSearch.jobSeeking}
            onCheckedChange={(checked) => handleDetailedSearchChange('jobSeeking', checked)}
          />
          <Label htmlFor="jobSeeking">구직자 여부</Label>
        </div>
        <div>
          <Label htmlFor="familyMembersCount">가구원 수</Label>
          <Select
            value={detailedSearch.familyMembersCount?.toString()}
            onValueChange={(value) => handleDetailedSearchChange('familyMembersCount', parseInt(value))}
          >
            <SelectTrigger id="familyMembersCount">
              <SelectValue placeholder="가구원 수 선택" />
            </SelectTrigger>
            <SelectContent>
              {[1, 2, 3, 4, 5, 6].map((num) => (
                <SelectItem key={num} value={num.toString()}>{num}인</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="flex items-center space-x-2">
          <Checkbox
            id="married"
            checked={detailedSearch.married}
            onCheckedChange={(checked) => handleDetailedSearchChange('married', checked)}
          />
          <Label htmlFor="married">기혼 여부</Label>
        </div>
        {detailedSearch.married && (
          <div>
            <Label htmlFor="marriageDate">결혼일</Label>
            <Input
              id="marriageDate"
              type="date"
              value={detailedSearch.marriageDate}
              onChange={(e) => handleDetailedSearchChange('marriageDate', e.target.value)}
            />
          </div>
        )}
        {detailedSearch.married && (
          <div className="flex items-center space-x-2">
            <Checkbox
              id="dualIncome"
              checked={detailedSearch.dualIncome}
              onCheckedChange={(checked) => handleDetailedSearchChange('dualIncome', checked)}
            />
            <Label htmlFor="dualIncome">맞벌이 여부</Label>
          </div>
        )}
        <div className="flex items-center space-x-2">
          <Checkbox
            id="hasChildren"
            checked={detailedSearch.hasChildren}
            onCheckedChange={(checked) => handleDetailedSearchChange('hasChildren', checked)}
          />
          <Label htmlFor="hasChildren">자녀 유무</Label>
        </div>
        {detailedSearch.hasChildren && (
          <div>
            <Label htmlFor="childrenCount">자녀 수</Label>
            <Input
              id="childrenCount"
              type="number"
              value={detailedSearch.childrenCount}
              onChange={(e) => handleDetailedSearchChange('childrenCount', parseInt(e.target.value))}
            />
          </div>
        )}
        {detailedSearch.hasChildren && (
          <div>
            <Label htmlFor="youngestChildBirthDate">막내 자녀 생년월일</Label>
            <Input
              id="youngestChildBirthDate"
              type="date"
              value={detailedSearch.youngestChildBirthDate}
              onChange={(e) => handleDetailedSearchChange('youngestChildBirthDate', e.target.value)}
            />
          </div>
        )}
        <div className="flex items-center space-x-2">
          <Checkbox
            id="singleParent"
            checked={detailedSearch.singleParent}
            onCheckedChange={(checked) => handleDetailedSearchChange('singleParent', checked)}
          />
          <Label htmlFor="singleParent">한부모 가정 여부</Label>
        </div>
        <div>
          <Label htmlFor="monthlyIncome">월 소득 (원)</Label>
          <Input
            id="monthlyIncome"
            type="number"
            value={detailedSearch.monthlyIncome}
            onChange={(e) => handleDetailedSearchChange('monthlyIncome', parseInt(e.target.value))}
          />
        </div>
        <div>
          <Label htmlFor="householdMonthlyIncome">가구 월 소득 (원)</Label>
          <Input
            id="householdMonthlyIncome"
            type="number"
            value={detailedSearch.householdMonthlyIncome}
            onChange={(e) => handleDetailedSearchChange('householdMonthlyIncome', parseInt(e.target.value))}
          />
        </div>
        <div className="flex items-center space-x-2">
          <Checkbox
            id="ownHouse"
            checked={detailedSearch.ownHouse}
            onCheckedChange={(checked) => handleDetailedSearchChange('ownHouse', checked)}
          />
          <Label htmlFor="ownHouse">주택 소유 여부</Label>
        </div>
        <div>
          <Label htmlFor="assets">자산 (원)</Label>
          <Input
            id="assets"
            type="number"
            value={detailedSearch.assets}
            onChange={(e) => handleDetailedSearchChange('assets', parseInt(e.target.value))}
          />
        </div>
        <div className="flex items-center space-x-2">
          <Checkbox
            id="ownCar"
            checked={detailedSearch.ownCar}
            onCheckedChange={(checked) => handleDetailedSearchChange('ownCar', checked)}
          />
          <Label htmlFor="ownCar">자동차 소유 여부</Label>
        </div>
        {detailedSearch.ownCar && (
          <div>
            <Label htmlFor="carPrice">자동차 가격 (원)</Label>
            <Input
              id="carPrice"
              type="number"
              value={detailedSearch.carPrice}
              onChange={(e) => handleDetailedSearchChange('carPrice', parseInt(e.target.value))}
            />
          </div>
        )}
        <div className="flex items-center space-x-2">
          <Checkbox
            id="hasSubscriptionAccount"
            checked={detailedSearch.hasSubscriptionAccount}
            onCheckedChange={(checked) => handleDetailedSearchChange('hasSubscriptionAccount', checked)}
          />
          <Label htmlFor="hasSubscriptionAccount">청약통장 보유 여부</Label>
        </div>
      </div>
      <Button onClick={saveDetailedSearch}>상세 검색 저장</Button>
    </div>
  )
}


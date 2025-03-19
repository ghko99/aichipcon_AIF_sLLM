import React, { useState } from 'react'
import { Button } from "@/components/ui/button"
import { ChevronUp, ChevronDown } from 'lucide-react'

interface AgeSelectorProps {
  value: string
  onChange: (age: string) => void
}

export const AgeSelector: React.FC<AgeSelectorProps> = ({ value, onChange }) => {
  const [selectedAge, setSelectedAge] = useState(value)
  const [inputAge, setInputAge] = useState(value === "19세 미만" || value === "65세 이상" ? "" : value);

  const handleAgeChange = (newAge: string) => {
    setInputAge(newAge);
    setSelectedAge(newAge);
    onChange(newAge);
  };

  const incrementAge = () => {
    const newAge = inputAge === '' ? '1' : (parseInt(inputAge) + 1).toString();
    handleAgeChange(newAge);
  };

  const decrementAge = () => {
    if (inputAge !== '' && parseInt(inputAge) > 1) {
      handleAgeChange((parseInt(inputAge) - 1).toString());
    }
  };

  return (
    <div className="flex items-center justify-center space-x-4">
      <Button
        variant="outline"
        size="icon"
        onClick={decrementAge}
        className="h-8 w-8 rounded-full"
      >
        <ChevronDown className="h-4 w-4" />
      </Button>
      <div className="relative w-24">
        <input
          type="text"
          value={inputAge}
          onChange={(e) => {
            const newValue = e.target.value.replace(/[^0-9]/g, '');
            handleAgeChange(newValue);
          }}
          className="text-2xl font-bold w-full text-center bg-transparent hover:bg-black hover:text-white transition-colors duration-200"
          placeholder=""
        />
      </div>
      <Button
        variant="outline"
        size="icon"
        onClick={incrementAge}
        className="h-8 w-8 rounded-full"
      >
        <ChevronUp className="h-4 w-4" />
      </Button>
    </div>
  )
}


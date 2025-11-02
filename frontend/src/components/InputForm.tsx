/**
 * Company Input Form Component
 * TODO: Implement form for company data collection
 */

import React from 'react';
import type { CompanyData } from '../lib/types';

interface InputFormProps {
  onAnalysisStart: (sessionId: string, companyData: CompanyData) => void;
}

const InputForm: React.FC<InputFormProps> = ({ onAnalysisStart: _onAnalysisStart }) => {
  // TODO: Implement state management
  // TODO: Implement form submission
  // TODO: Implement error handling

  return (
    <div>
      <h2>TODO: Company Input Form</h2>
      <p>Fields needed: company_name, website, founder_github, industry, product_description</p>
    </div>
  );
};

export default InputForm;

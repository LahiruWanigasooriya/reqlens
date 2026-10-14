export type User = {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
};

export type Project = {
  id: string;
  name: string;
  description: string | null;
  status: string;
  created_at: string;
  updated_at: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export type ProjectFile = {
  id: string;
  project_id: string;
  original_name: string;
  file_type: string;
  mime_type: string | null;
  size_bytes: number;
  processing_status: string;
  processing_error: string | null;
  created_at: string;
};

export type VerifiableCriterion = {
  id: string;
  criterion_number: number;
  description: string;
  expected_behavior: string | null;
  constraint_text: string | null;
};


export type Requirement = {
  id: string;
  external_id: string;
  title: string;
  description: string;
  requirement_type: string;
  source_text: string | null;
  created_at: string;
  criteria: VerifiableCriterion[];
};
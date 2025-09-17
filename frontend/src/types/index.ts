export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  is_active: boolean;
  date_joined: string;
  profile?: UserProfile;
}

export interface UserProfile {
  id: number;
  user: number;
  profile_picture?: string;
  address?: string;
  date_of_birth?: string;
  emergency_contact?: string;
}

export interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
  message: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  password_confirm: string;
  phone?: string;
}

export interface Institute {
  id: number;
  name: string;
  subdomain: string;
  code: string;
  address: string;
  phone: string;
  email: string;
  website?: string;
  logo?: string;
  established_date: string;
  is_active: boolean;
}

export interface Role {
  id: number;
  name: 'admin' | 'faculty' | 'student' | 'guest';
  description?: string;
  permissions: string[];
}
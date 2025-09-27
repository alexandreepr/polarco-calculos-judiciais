interface AuthContextType {
  accessToken: string | null;
  currentUser: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}
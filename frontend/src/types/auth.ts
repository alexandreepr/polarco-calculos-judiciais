interface AuthContextType {
  accessToken: string | null;
  currentUser: User | null;
  loadingAuth: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}
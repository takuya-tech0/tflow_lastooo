import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { loginUser } from '../utils/api';

export default function useAuth() {
    const [user, setUser] = useState(null);
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            // Validate token and set user
        }
    }, []);

    const login = async (username, password) => {
        try {
            const data = await loginUser(username, password);
            localStorage.setItem('token', data.access_token);
            setUser(data.user);
            return data;
        } catch (error) {
            throw new Error('ログインに失敗しました。ユーザー名とパスワードを確認してください。');
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
        router.push('/login');
    };

    return { user, login, logout };
}
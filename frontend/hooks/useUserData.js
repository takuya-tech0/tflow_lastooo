import { useState, useEffect } from 'react';
import axios from 'axios';

export default function useUserData() {
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/users/me`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                setUserData(response.data);
            } catch (error) {
                console.error('Failed to fetch user data:', error);
                setError('ユーザー情報の取得に失敗しました。');
            }
        };
    
        fetchUserData();
    }, []);

    return { userData, error };
}
import axios from 'axios';
import { API_URL } from '../constants/config';

export const loginUser = async (username, password) => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    try {
        const response = await axios.post(`${API_URL}/token`, params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        if (error.response) {
            throw new Error('ログインに失敗しました。ユーザー名とパスワードを確認してください。');
        } else if (error.request) {
            throw new Error('サーバーに接続できません。ネットワーク接続を確認してください。');
        } else {
            throw new Error('予期せぬエラーが発生しました。もう一度お試しください。');
        }
    }
};
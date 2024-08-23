import { useState } from 'react';
import { useRouter } from 'next/router';
import { motion, AnimatePresence } from 'framer-motion';
import useAuth from '../hooks/useAuth';
import ErrorMessage from './ErrorMessage';
import styles from '../styles/Login.module.css';

export default function LoginForm({ setIsSuccess, isSuccess }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await login(username, password);
            setIsSuccess(true);
            setTimeout(() => {
                router.push('/mypage');
            }, 1000);
        } catch (error) {
            setError(error.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <motion.form
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            onSubmit={handleSubmit}
            className={styles.form}
        >
            <div className={styles.inputGroup}>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    required
                />
            </div>
            <div className={styles.inputGroup}>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                />
            </div>
            <div className={styles.inputGroup}>
                <button type="submit" disabled={isLoading || isSuccess}>
                    {isLoading ? 'Logging in...' : isSuccess ? 'Success!' : 'Log in'}
                </button>
            </div>
            <AnimatePresence>
                {error && <ErrorMessage message={error} />}
            </AnimatePresence>
        </motion.form>
    );
}
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import useAuth from '../hooks/useAuth';
import Layout from '../components/Layout';
import styles from '../styles/Home.module.css';

export default function Home() {
  const router = useRouter();
  const { user } = useAuth();

  useEffect(() => {
    if (!user) {
      router.push('/login');
    }
  }, [user, router]);

  if (!user) {
    return null; // または loading spinner
  }

  return (
    <Layout>
      <div className={styles.container}>
        <main className={styles.main}>
          <h1 className={styles.title}>
            Welcome to <a href="https://nextjs.org">Talent Flow</a>
          </h1>

          <p className={styles.description}>
            AIによる最適な人事配置を実現
          </p>

          <div className={styles.grid}>
            <a href="/job_recommendation" className={styles.card}>
              <h2>Job Recommendations &rarr;</h2>
              <p>Find the best job matches based on your skills and experience.</p>
            </a>

            <a href="/mypage" className={styles.card}>
              <h2>My Page &rarr;</h2>
              <p>View and update your profile information.</p>
            </a>

            {/* Add more cards for other features */}
          </div>
        </main>
      </div>
    </Layout>
  );
}
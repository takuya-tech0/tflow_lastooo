import React from 'react';
import { useRouter } from 'next/router';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/Layout';
import UserProfile from '../components/UserProfile';
import PsychographicChart from '../components/PsychographicChart';
import CareerInfo from '../components/CareerInfo';
import LoadingSpinner from '../components/LoadingSpinner';
import useUserData from '../hooks/useUserData';
import styles from '../styles/MyPage.module.css';

export default function MyPage() {
  const router = useRouter();
  const { userData, loading, error } = useUserData();

  const handleRecommendationClick = (type) => {
    if (type === 'personality') {
      router.push('/job_recommendation_personality');
    } else if (type === 'career') {
      router.push('/job_recommendation_skill');
    }
  };

  return (
    <Layout>
      <div className={styles.mypageContainer}>
        <AnimatePresence>
          {loading ? (
            <LoadingSpinner key="loading" />
          ) : error ? (
            <motion.p
              key="error"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className={styles.error}
            >
              {error}
            </motion.p>
          ) : userData && (
            <motion.div
              key="content"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className={styles.contentWrapper}
            >
              <div className={styles.profileSection}>
                <UserProfile userData={userData} />
              </div>
              <main className={styles.mainContent}>
                <div className={styles.sectionContainer}>
                  <section className={styles.section}>
                    <PsychographicChart spiData={userData.spi} />
                  </section>
                  <section className={styles.section}>
                    <h2>性格情報</h2>
                    <CareerInfo personality_detail={userData.employee_info.personality_detail} />
                  </section>
                </div>
                <div className={styles.buttons}>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => alert('評価・コメント閲覧')}
                  >
                    評価・コメント閲覧
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleRecommendationClick('personality')}
                  >
                    性格傾向によるマッチング
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleRecommendationClick('career')}
                  >
                    スキルによるマッチング
                  </motion.button>
                </div>
              </main>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Layout>
  );
}
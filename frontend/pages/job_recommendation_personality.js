import React from 'react';
import Layout from '../components/Layout';
import UserProfile from '../components/UserProfile';
import JobRecommendationCard from '../components/JobRecommendationCard';
import useUserData from '../hooks/useUserData';
import styles from '../styles/JobRecommendation.module.css';

export default function JobRecommendationPersonality() {
    const { userData, error: userDataError } = useUserData();

    if (userDataError) {
        return <div className={styles.error}>Error: {userDataError}</div>;
    }

    if (!userData) {
        return <div className={styles.loading}>Loading...</div>;
    }

    return (
        <Layout>
            <div className={styles.jobRecommendationContainer}>
                <div className={styles.content}>
                    <UserProfile userData={userData} />
                    <main className={styles.mainContent}>
                        <h2>性格傾向によるマッチング</h2>
                        <JobRecommendationCard
                            userData={userData}
                            recommendationType="personality"
                        />
                    </main>
                </div>
            </div>
        </Layout>
    );
}
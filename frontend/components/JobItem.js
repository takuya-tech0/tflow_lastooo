// JobItem.js
import { useState } from 'react';
import { motion } from 'framer-motion';
import styles from '../styles/JobItem.module.css';

export default function JobItem({ job, index }) {
    const [showDetails, setShowDetails] = useState(false);

    const toggleDetails = () => {
        setShowDetails(!showDetails);
    };

    return (
        <motion.div
            className={styles.jobCard}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
        >
            <div className={styles.jobHeader}>
                <div className={styles.jobInfo}>
                    <h4 className={styles.jobTitle}>{job.job_title} ({job.similarity}% match)</h4>
                    <p className={styles.jobDepartment}>Department: {job.department_name}</p>
                    <div className={styles.skills}>
                        {job.skills.map((skill, idx) => (
                            <span key={idx} className={styles.skill}>{skill}</span>
                        ))}
                    </div>
                </div>

                {/* 「詳細を見る」ボタンを追加 */}
                <button onClick={toggleDetails} className={styles.detailsButton}>
                    {showDetails ? '閉じる' : '詳細を見る'}
                </button>
            </div>

            {/* 詳細が開いた場合に表示される部分 */}
            {showDetails && (
                <div className={styles.jobDetails}>
                    <p>{job.job_detail}</p>
                    <p><strong>マッチング理由:</strong></p>
                    <ul>
                        {job.matching_reasons && job.matching_reasons.length > 0 ? (
                            job.matching_reasons.map((reason, idx) => (
                                <li key={idx}>{reason}</li>
                            ))
                        ) : (
                            <li>マッチング理由はありません</li>
                        )}
                    </ul>
                </div>
            )}
        </motion.div>
    );
}

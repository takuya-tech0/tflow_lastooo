// JobCard.js
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styles from '../styles/JobCard.module.css';

const JobCard = ({ job }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    return (
        <>
            <div className={styles.jobCard}>
                <p className={styles.department}>{job.department_name}部</p>
                <h3 className={styles.jobTitle}>{job.job_title || `求人ID: ${job.job_id}`}</h3>
                <p className={styles.similarity}>マッチ度: {job.similarity.toFixed(2)}%</p>
                <button onClick={openModal} className={styles.detailsButton}>
                    詳細を見る
                </button>
            </div>

            <AnimatePresence>
                {isModalOpen && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className={styles.modalOverlay}
                        onClick={closeModal}
                    >
                        <motion.div
                            className={styles.modalContent}
                            onClick={(e) => e.stopPropagation()}
                            initial={{ y: 50, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            exit={{ y: 50, opacity: 0 }}
                        >
                            <h2 className={styles.modalTitle}>{job.job_title || `求人ID: ${job.job_id}`}</h2>
                            <h3 className={styles.modalDepartment}>{job.department_name}部</h3>
                            {job.job_detail && (
                                <>
                                    <h4 className={styles.sectionTitle}>職務内容:</h4>
                                    <p className={styles.jobDetail}>{job.job_detail}</p>
                                </>
                            )}
                            <h4 className={styles.sectionTitle}>マッチング理由:</h4>
                            <ul className={styles.matchingReasons}>
                                {job.matching_reasons && job.matching_reasons.map((reason, index) => (
                                    <li key={index} className={styles.matchingReason}>{reason}</li>
                                ))}
                            </ul>
                            <button onClick={closeModal} className={styles.closeButton}>
                                閉じる
                            </button>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
};

export default JobCard;
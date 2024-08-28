import React from 'react';
import { motion } from 'framer-motion';

const UserProfile = ({ userData }) => {
    if (!userData || !userData.employee_info) {
        return <div>Loading user data...</div>;
    }

    return (
        <motion.aside
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white shadow-lg rounded-lg p-6 m-4"
        >
            <h2 className="text-2xl font-bold mb-4">ユーザープロフィール</h2>
            <ul className="space-y-2">
                <li><strong>氏名:</strong> {userData.employee_info.name}</li>
                <li><strong>社員番号:</strong> {userData.employee_info.id}</li>
                <li>
                    <strong>部署:</strong> 
                    {userData.departments && userData.departments.length > 0
                        ? userData.departments[0].department_name
                        : "所属部署なし"}
                </li>
                <li><strong>入社日:</strong> {userData.employee_info.hire_date}</li>
                <li><strong>学歴:</strong> {userData.employee_info.academic_background}</li>
            </ul>
        </motion.aside>
    );
};

export default UserProfile;
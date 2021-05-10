import React from 'react';
import { Link } from 'react-router-dom';
import './navigation.styles.css';
const Navigation = () => (
    <div className="navigation">
        <Link className="nav-item" to="add-transaction">Add Transaction</Link>
    </div>
)

export default Navigation;
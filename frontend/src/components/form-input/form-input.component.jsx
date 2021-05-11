import React from 'react';

const FormInput = ({ type, label, name, value, handleChange, min, step }) => (
    <input type={type} name={name} value={value} placeholder={label} onChange={handleChange} min={min} step={step} />
)

export default FormInput;
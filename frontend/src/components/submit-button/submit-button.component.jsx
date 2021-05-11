import React from 'react';

const SubmitButton = ({ submit, children }) => (
    <button onClick={submit} type="button">{children}</button>
)

export default SubmitButton;
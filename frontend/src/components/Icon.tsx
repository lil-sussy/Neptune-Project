import React from 'react';

export const EditIcon = () => (
  <svg width="10" height="13" viewBox="0 0 10 13" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3.77013 9.12775L1 10L1.77564 6.88483L6.84804 1.20828C6.90535 1.14235 6.97387 1.08996 7.0494 1.05419C7.12499 1.01842 7.20619 1 7.28819 1C7.37018 1 7.45138 1.01842 7.52697 1.05419C7.6025 1.08996 7.67102 1.14235 7.72833 1.20828L8.81791 2.44051C8.87559 2.50486 8.92139 2.58143 8.95266 2.66579C8.98393 2.75015 9 2.84063 9 2.93202C9 3.0234 8.98393 3.11389 8.95266 3.19825C8.92139 3.28261 8.87559 3.35917 8.81791 3.42352L3.77013 9.12775Z" stroke="#F8CD4B" strokeLinecap="round" strokeLinejoin="round"/>
    <rect y="12" width="9" height="1" rx="0.5" fill="#F8CD4B"/>
  </svg>
);

export const CardIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="14" cy="14" r="14" fill="#F8CD4B" fillOpacity="0.15"/>
    <path d="M19.5 19.5C19.5 19.7652 19.3946 20.0196 19.2071 20.2071C19.0196 20.3946 18.7652 20.5 18.5 20.5H9.5C9.23478 20.5 8.98043 20.3946 8.79289 20.2071C8.60536 20.0196 8.5 19.7652 8.5 19.5V8.5C8.5 8.23478 8.60536 7.98043 8.79289 7.79289C8.98043 7.60536 9.23478 7.5 9.5 7.5H16L19.5 11V19.5Z" stroke="#F8CD4B" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M15.5 7.5V11.5H19.5" stroke="#F8CD4B" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const Icons = { Icon1: EditIcon, Icon2: CardIcon };
export default Icons;

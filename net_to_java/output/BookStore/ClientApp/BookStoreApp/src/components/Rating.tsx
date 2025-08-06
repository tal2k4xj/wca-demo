// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
import React from 'react';

interface Props {
  rating: number;
}

export const Rating: React.FC<Props> = ({ rating }) => {
  const stars = Array.from({ length: rating }, (_, index) => index + 1);

  return (
    <div className="rating">
      {stars.map((star) => (
        <span key={star} className="star">
          ★
        </span>
      ))}
    </div>
  );
};
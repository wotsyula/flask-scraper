import React from 'react';

const Person = ({
    url,
    text,
} = {}) => {
    let description = (/linkedin/.test(url))
        ? 'Linkedin'
        : (/twitter/.test(url))
            ? 'Twitter'
            : (/facebook/.test(url))
                ? 'Facebook'
                : 'Unknown';

    return (
        <div className="content">
            <div className="Header">
                <a href={url}>{text}</a>
            </div>
            <div className="description">
                {description}
            </div>
        </div>
    );
};

export default Person;

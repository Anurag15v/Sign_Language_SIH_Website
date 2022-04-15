import React, { useState } from 'react';
import classNames from 'classnames';
import { SectionProps } from '../../utils/SectionProps';
import Functionality from "../../views/Functionality"
import good from "../../assets/images/good-sign.png"
import language from "../../assets/images/language.png"
const propTypes = {
  ...SectionProps.types
}

const defaultProps = {
  ...SectionProps.defaults
}

const Hero = ({
  className,
  topOuterDivider,
  bottomOuterDivider,
  topDivider,
  bottomDivider,
  hasBgColor,
  invertColor,
  ...props
}) => {

  const [videoModalActive, setVideomodalactive] = useState(false);

  const openModal = (e) => {
    e.preventDefault();
    setVideomodalactive(true);
  }

  const closeModal = (e) => {
    e.preventDefault();
    setVideomodalactive(false);
  }

  const outerClasses = classNames(
    'hero section center-content',
    topOuterDivider && 'has-top-divider',
    bottomOuterDivider && 'has-bottom-divider',
    hasBgColor && 'has-bg-color',
    invertColor && 'invert-color',
    className
  );

  const innerClasses = classNames(
    'hero-inner section-inner',
    topDivider && 'has-top-divider',
    bottomDivider && 'has-bottom-divider'
  );

  return (
    <section
      {...props}
      className={outerClasses}
    >
      <div className="container-sm">
        <div >
          <div className="hero-content">
            <h2 className="mt-0 mb-16 reveal-from-bottom" data-reveal-delay="200">
              Powerful Sign Language Detection Software
              <span style={{ fontSize: "40px" }} className="text-color-primary"> वार्तालाप</span>
            </h2>
            <img style={{ height: "200px", width: "200px", position: "absolute", left: "50px", transform: "rotate(-45deg)" }} src={good} />
            <img style={{ height: "200px", width: "80vh", position: "absolute", right: "-150px", transform: "rotate(90deg)" }} src={language} />
            <div className="container-xs">
              <p className="m-0 mb-32 reveal-from-bottom" data-reveal-delay="400">
                Sign Language Detection software with Sign to Text and Speech to Sign Modes.<span style={{ color: "white" }}>Let's unite to support our specially abled friends.</span>
              </p>
              <Functionality />
            </div>
          </div>
        </div>
      </div>
    </section >
  );
}

Hero.propTypes = propTypes;
Hero.defaultProps = defaultProps;

export default Hero;
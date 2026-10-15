import React from 'react';
import {Composition} from 'remotion';
import {Reels, ReelsProps, toplamSure, FPS} from './Reels';

export const Root: React.FC = () => (
  <Composition
    id="Reels"
    component={Reels as any}
    width={1080}
    height={1920}
    fps={FPS}
    durationInFrames={300}
    defaultProps={{} as any}
    calculateMetadata={({props}) => ({durationInFrames: Math.round(toplamSure(props as unknown as ReelsProps) * FPS)})}
  />
);

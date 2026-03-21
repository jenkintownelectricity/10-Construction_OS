/**
 * Construction OS — Mock Voice Adapter Seam
 * MOCK: Voice adapter is a seam only. No real voice integration in this wave.
 */

import type { VoiceAdapter, VoiceCommand } from '../contracts/adapters';

export const mockVoice: VoiceAdapter = {
  adapterName: 'mock-voice',
  isMock: true,
  isAvailable: false,

  async startListening() {
    console.warn('[MockVoice] Voice adapter is a mock seam — not available');
  },

  async stopListening() {
    // no-op
  },

  onCommand(_handler: (command: VoiceCommand) => void) {
    // Return unsubscribe no-op
    return () => {};
  },
};

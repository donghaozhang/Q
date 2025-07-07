import { agentPlaygroundFlagFrontend } from '@/flags';
import { isFlagEnabled } from '@/lib/feature-flags';
import { Metadata } from 'next';
import { redirect } from 'next/navigation';

export const metadata: Metadata = {
  title: 'Agent Conversation | Quriosity Q',
  description: 'Interactive agent conversation powered by Quriosity Q',
  openGraph: {
    title: 'Agent Conversation | Quriosity Q',
    description: 'Interactive agent conversation powered by Quriosity Q',
    type: 'website',
  },
};

export default async function AgentsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}

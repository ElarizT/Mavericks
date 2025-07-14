import { Zap } from 'lucide-react';

export default function TopBanner() {
  return (
    <div className='w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-2 px-4 flex justify-center items-center text-center'>
      <span className='flex items-center gap-2 font-semibold text-lg'>
        <Zap className='w-6 h-6 inline-block' />
        Empower your legal workflow with LawCo AI!
      </span>
    </div>
  );
}

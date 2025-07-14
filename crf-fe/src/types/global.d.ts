declare module "lucide-react" {
  import { ForwardRefExoticComponent, RefAttributes, SVGProps } from "react";

  export interface LucideProps extends SVGProps<SVGSVGElement> {
    size?: number | string;
    absoluteStrokeWidth?: boolean;
  }

  export type LucideIcon = ForwardRefExoticComponent<
    LucideProps & RefAttributes<SVGSVGElement>
  >;

  export const Bot: LucideIcon;
  export const User: LucideIcon;
  export const FileText: LucideIcon;
  export const Image: LucideIcon;
  export const File: LucideIcon;
  export const Paperclip: LucideIcon;
  export const X: LucideIcon;
  export const Send: LucideIcon;
  export const Upload: LucideIcon;
  export const AlertCircle: LucideIcon;
  export const Wifi: LucideIcon;
  export const WifiOff: LucideIcon;
  export const Loader2: LucideIcon;
  export const MessageCircle: LucideIcon;
  export const Sparkles: LucideIcon;
  export const Shield: LucideIcon;
  export const Zap: LucideIcon;
  export const ArrowRight: LucideIcon;
  export const ArrowLeft: LucideIcon;
  export const Settings: LucideIcon;
  export const MessageSquare: LucideIcon;
  export const Plus: LucideIcon;
  export const ChevronLeft: LucideIcon;
  export const ChevronRight: LucideIcon;
}

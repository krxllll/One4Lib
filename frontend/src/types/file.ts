export type File = {
  id: string
  author_username: string
  title: string
  description: string
  file_type: FileType
  price: number
  tags: string[]
  purchase_count: number
  upload_date: string
  thumbnail_url: string
  preview_url: string
  file_url: string
  viewer_status: string
}

export const fileTypes = [
  'application/pdf',
  'application/doc',
  'application/xlsx',
  'image/jpg',
  'image/png',
  'image/svg',
  'audio/mp3',
  'audio/mp4',
  'code/py',
  'code/cpp',
] as const

export type FileType = typeof fileTypes[number]

export const fileTypeColors: Record<string, string> = {
  application: 'bg-green',
  image: 'bg-red',
  audio: 'bg-blue',
  code: 'bg-purple',
}

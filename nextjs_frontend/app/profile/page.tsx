import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export default function Profile() {
  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader className="flex flex-row items-center gap-4">
          <Avatar className="w-20 h-20">
            <AvatarImage src="/placeholder-avatar.jpg" alt="User's avatar" />
            <AvatarFallback>UN</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle className="text-2xl">User Name</CardTitle>
            <p className="text-muted-foreground">user@example.com</p>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">About Me</h3>
            <p>This is a brief description about the user. It can be edited to include more information.</p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2">Account Details</h3>
            <p><strong>Joined:</strong> January 1, 2023</p>
            <p><strong>Last Login:</strong> July 15, 2023</p>
          </div>
          <Button>Edit Profile</Button>
        </CardContent>
      </Card>
    </div>
  )
}
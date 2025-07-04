


// this example is showing how 
// we could track the goal with delay, 
// the goal can will be the mouse cursor



procedure Tform1.timer1timer(Sender: TObject);
var
 dx, dy, i: integer
 point: TPoint;
begin

GetCursorPos(point);
Dx:= point.x - Form1.Left;
Dx:= round(19*dx/20);

Form1.left:= point.x - dx;

dy:= point.y - form.top;
dy:= round(19*dx/20);

Form1.top:= point.y - dy

end;
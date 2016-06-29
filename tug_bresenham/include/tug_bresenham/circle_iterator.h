#ifndef _TUG_BRESENHAM__CIRCLE_ITERATOR_H_
#define _TUG_BRESENHAM__CIRCLE_ITERATOR_H_

namespace tug_bresenham
{

/**
 * Implementation of the Bresenham circle algorithm in iterator form.
 *
 * Due to the nature of the algorithm, results are returned as the coordinates
 * of points (dx, dy) on a circle of the given radius centered at (0, 0), for
 * the first quadrant. To get a full circle, you have to consider all four
 * combinations of (+-dx, +-dy). Note that (dx, dy) will be invalid values
 * once isFinished() returns true.
 */
class CircleIterator
{
public:
  CircleIterator(int radius);

  void operator++();
  void operator++(int);

  inline int getDx() const
  {
    return dx_;
  }

  inline int getDy() const
  {
    return dy_;
  }

  bool isFinished() const;

protected:
  void advance();

  int dx_;
  int dy_;
  long r_squared_;
  long error_;
};

}

#endif

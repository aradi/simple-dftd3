! This file is part of s-dftd3.
!
! Copyright (C) 2019 Sebastian Ehlert
!
! s-dftd3 is free software: you can redistribute it and/or modify it under
! the terms of the GNU General Public License as published by
! the Free Software Foundation, either version 3 of the License, or
! (at your option) any later version.
!
! s-dftd3 is distributed in the hope that it will be useful,
! but WITHOUT ANY WARRANTY; without even the implied warranty of
! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
! GNU General Public License for more details.
!
! You should have received a copy of the GNU General Public License
! along with s-dftd3.  If not, see <https://www.gnu.org/licenses/>.

module d3par_constants
   use iso_fortran_env, only: wp => real64
   implicit none

   !> ratio of a circle's circumference to its diameter
   real(wp), parameter :: pi = 4.0_wp * atan(1.0_wp)
   !> √π
   real(wp), parameter :: sqrtpi = sqrt(pi)
   !> 2×π
   real(wp), parameter :: twopi = 2.0_wp * pi
   !> 4×π
   real(wp), parameter :: fourpi = 4.0_wp * pi
   !> π/2
   real(wp), parameter :: pihalf = 0.5_wp * pi

end module d3par_constants

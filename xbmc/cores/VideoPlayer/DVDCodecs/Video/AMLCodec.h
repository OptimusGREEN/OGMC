#pragma once
/*
 *      Copyright (C) 2005-2013 Team XBMC
 *      http://xbmc.org
 *
 *  This Program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2, or (at your option)
 *  any later version.
 *
 *  This Program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with XBMC; see the file COPYING.  If not, see
 *  <http://www.gnu.org/licenses/>.
 *
 */

#include "DVDVideoCodec.h"
#include "cores/VideoPlayer/DVDStreamInfo.h"
#include "cores/IPlayer.h"
#include "guilib/Geometry.h"
#include "rendering/RenderSystem.h"
#include "threads/Thread.h"

#define AML_NUM_BUFFERS 3
#define AML_PTS_FREQ        90000

typedef struct am_private_t am_private_t;

class DllLibAmCodec;

class IVPClockCallback;

class CAMLCodec : public CThread
{
  friend class CDVDVideoCodecAmlogic;
public:
  CAMLCodec();
  virtual ~CAMLCodec();

  bool          OpenDecoder(CDVDStreamInfo &hints);
  void          CloseDecoder();
  void          Reset();

  int           Decode(uint8_t *pData, size_t size, double dts, double pts);

  bool          GetPicture(DVDVideoPicture* pDvdVideoPicture);
  void          SetSpeed(int speed);
  int           GetDataSize();
  double        GetTimeSize();
  void          SetVideoRect(const CRect &SrcRect, const CRect &DestRect);

protected:
  virtual void  Process();
  int64_t          m_start_dts;
  int64_t          m_start_pts;
  volatile int64_t m_cur_pts;

private:
  void          SetVideoPtsSeconds(double pts);
  void          ShowMainVideo(const bool show);
  void          SetVideoZoom(const float zoom);
  void          SetVideoContrast(const int contrast);
  void          SetVideoBrightness(const int brightness);
  void          SetVideoSaturation(const int saturation);
  bool          SetVideo3dMode(const int mode3d);
  std::string   GetStereoMode();

  DllLibAmCodec   *m_dll;
  bool             m_opened;
  am_private_t    *am_private;
  CDVDStreamInfo   m_hints;
  volatile int     m_speed;
  volatile int64_t m_1st_pts;
  volatile int64_t m_cur_pictcnt;
  volatile int64_t m_old_pictcnt;
  volatile double  m_timesize;
  volatile int64_t m_vbufsize;
  CEvent           m_ready_event;

  CRect            m_dst_rect;
  CRect            m_display_rect;

  int              m_view_mode;
  RENDER_STEREO_MODE m_stereo_mode;
  RENDER_STEREO_VIEW m_stereo_view;
  float            m_zoom;
  int              m_contrast;
  int              m_brightness;
};

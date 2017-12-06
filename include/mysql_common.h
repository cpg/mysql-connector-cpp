/*
* Copyright (c) 2015, 2017, Oracle and/or its affiliates. All rights reserved.
*
* The MySQL Connector/C++ is licensed under the terms of the GPLv2
* <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
* MySQL Connectors. There are special exceptions to the terms and
* conditions of the GPLv2 as it is applied to this software, see the
* FLOSS License Exception
* <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
*
* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published
* by the Free Software Foundation; version 2 of the License.
*
* This program is distributed in the hope that it will be useful, but
* WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
* or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
* for more details.
*
* You should have received a copy of the GNU General Public License along
* with this program; if not, write to the Free Software Foundation, Inc.,
* 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA
*/

#ifndef MYSQL_COMMON_H
#define MYSQL_COMMON_H

/*
  Common definitions and declarations that are needed by public headers.

  Note: Any common stuff that is needed only by the implementation, should be
  kept in the common/ folder, either as headers or source files.
*/

#include "common/api.h"
#include "common/error.h"
#include "common/util.h"
#include "common/value.h"


#define DEFAULT_MYSQL_PORT  3306
#define DEFAULT_MYSQLX_PORT 33060

#undef min
#undef max

// ----------------------------------------------------------------------------

/*
  Common constants
  ================

  Warning: Values of these constants are part of the public API. Changing them
  is a non backward compatible API change.

  Note: Value of 0 is reserved for special uses and thus constant values
  are always > 0.
*/

/*
  Note: the empty END_LIST macro at the end of list macros helps Doxygen
  correctly interpret documentation for the list item.
*/

#undef END_LIST
#define END_LIST


#define SESSION_OPTION_LIST(x)                                               \
  OPT_STR(x,URI,1)         /*!< connection URI or string */                  \
  /*! DNS name of the host, IPv4 address or IPv6 address */                  \
  OPT_STR(x,HOST,2)                                                          \
  OPT_NUM(x,PORT,3)        /*!< X Plugin port to connect to */               \
  /*! Assign a priority (a number in range 1 to 100) to the last specified
      host; these priorities are used to determine the order in which multiple
      hosts are tried by the connection fail-over logic (see description
      of `Session` class) */                                                 \
  OPT_NUM(x,PRIORITY,4)                                                      \
  OPT_STR(x,USER,5)        /*!< user name */                                 \
  OPT_STR(x,PWD,6)         /*!< password */                                  \
  OPT_STR(x,DB,7)          /*!< default database */                          \
  OPT_ANY(x,SSL_MODE,8)    /*!< define `SSLMode` option to be used */        \
  /*! path to a PEM file specifying trusted root certificates*/              \
  OPT_STR(x,SSL_CA,9)                                                        \
  OPT_ANY(x,AUTH,10)      /*!< authentication method, PLAIN, MYSQL41, etc.*/ \
  OPT_STR(x,SOCKET,11)
  END_LIST

#define OPT_STR(X,Y,N) X##_str(Y,N)
#define OPT_NUM(X,Y,N) X##_num(Y,N)
#define OPT_ANY(X,Y,N) X##_any(Y,N)


/*
  Names for options supported in the query part of a connection string and
  how they map to session options above.
*/

#define URI_OPTION_LIST(X)  \
  X("ssl-mode", SSL_MODE)   \
  X("ssl-ca", SSL_CA)       \
  X("auth", AUTH)           \
  END_LIST


#define SSL_MODE_LIST(x) \
  x(DISABLED,1)        /*!< Establish an unencrypted connection.  */ \
  x(REQUIRED,2)        /*!< Establish a secure connection if the server supports
                          secure connections. The connection attempt fails if a
                          secure connection cannot be established. This is the
                          default if `SSL_MODE` is not specified. */ \
  x(VERIFY_CA,3)       /*!< Like `REQUIRED`, but additionally verify the server
                          TLS certificate against the configured Certificate
                          Authority (CA) certificates (defined by `SSL_CA`
                          Option). The connection attempt fails if no valid
                          matching CA certificates are found.*/ \
  x(VERIFY_IDENTITY,4) /*!< Like `VERIFY_CA`, but additionally verify that the
                          server certificate matches the host to which the
                          connection is attempted.*/\
  END_LIST


#define AUTH_METHOD_LIST(x)\
  x(PLAIN,1)       /*!< Plain text authentication method. The password is
                      sent as a clear text. This method is used by
                      default in encrypted connections. */ \
  x(MYSQL41,2)     /*!< Authentication method supported by MySQL 4.1 and newer.
                      The password is hashed before being sent to the server.
                      This method is used by default in unencrypted
                      connections */ \
  x(EXTERNAL,3)    /*!< External authentication when the server establishes
                      the user authenticity by other means such as SSL/x509
                      certificates. Currently not supported by X Plugin */ \
  END_LIST

/*
  Types that can be reported by MySQL server.
*/

#define RESULT_TYPE_LIST(X) \
  X(BIT,        1)   \
  X(TINYINT,    2)   \
  X(SMALLINT,   3)   \
  X(MEDIUMINT,  4)   \
  X(INT,        5)   \
  X(BIGINT,     6)   \
  X(FLOAT,      7)   \
  X(DECIMAL,    8)   \
  X(DOUBLE,     9)   \
  X(JSON,       10)  \
  X(STRING,     11)  \
  X(BYTES,      12)  \
  X(TIME,       13)  \
  X(DATE,       14)  \
  X(DATETIME,   15)  \
  X(TIMESTAMP,  16)  \
  X(SET,        17)  \
  X(ENUM,       18)  \
  X(GEOMETRY,   19)  \
  END_LIST


/*
  Check options for an updatable view.
  @see https://dev.mysql.com/doc/refman/en/view-check-option.html
*/

#define VIEW_CHECK_OPTION_LIST(x) \
  x(CASCADED,1) \
  x(LOCAL,2) \
  END_LIST

/*
  Algorithms used to process views.
  @see https://dev.mysql.com/doc/refman/en/view-algorithms.html
*/

#define VIEW_ALGORITHM_LIST(x) \
  x(UNDEFINED,1) \
  x(MERGE,2) \
  x(TEMPTABLE,3) \
  END_LIST

/*
  View security settings.
  @see https://dev.mysql.com/doc/refman/en/stored-programs-security.html
*/

#define VIEW_SECURITY_LIST(x) \
  x(DEFINER,1) \
  x(INVOKER,2) \
  END_LIST


#define LOCK_MODE_LIST(X) \
  X(SHARED,1)    \
  X(EXCLUSIVE,2) \
  END_LIST

// ----------------------------------------------------------------------------

/*
  Warning! must be included after above constant definitions.
*/

#include "common/settings.h"

/*
  On Windows, dependency on the sockets library can be handled using
  #pragma comment directive.
*/

#ifdef _WIN32
#pragma comment(lib,"ws2_32")
#endif


#endif